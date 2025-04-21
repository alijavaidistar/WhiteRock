from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import SignUpForm
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        # Create test users with each role
        self.basic_user = User.objects.create_user(
            username='testbasic',
            email='basic@example.com',
            password='testpassword123',
            role='basic'
        )
        
        self.staff_user = User.objects.create_user(
            username='naim_m',
            email='staff@example.com',
            password='Iambasic',
            role='staff'
        )
        
        self.admin_user = User.objects.create_user(
            username='iamadmin34',
            email='admin@example.com',
            password='admin123#124)',
            role='admin'
        )
    
    def test_user_creation(self):
        """Test users can be created with correct attributes"""
        # Basic user
        self.assertEqual(self.basic_user.username, 'testbasic')
        self.assertEqual(self.basic_user.email, 'basic@example.com')
        self.assertEqual(self.basic_user.role, 'basic')
        self.assertTrue(self.basic_user.check_password('testpassword123'))
        
        # Staff user
        self.assertEqual(self.staff_user.username, 'naim_m')
        self.assertEqual(self.staff_user.role, 'staff')
        self.assertTrue(self.staff_user.check_password('Iambasic'))
        
        # Admin user
        self.assertEqual(self.admin_user.username, 'iamadmin34')
        self.assertEqual(self.admin_user.role, 'admin')
        self.assertTrue(self.admin_user.check_password('admin123#124)'))
    
    def test_user_string_representation(self):
        """Test the string representation of User objects"""
        self.assertEqual(str(self.basic_user), 'testbasic (basic)')
        self.assertEqual(str(self.staff_user), 'naim_m (staff)')
        self.assertEqual(str(self.admin_user), 'iamadmin34 (admin)')

class UserAuthViewsTest(TestCase):
    def setUp(self):
        # Set up test site
        site = Site.objects.get_or_create(domain='example.com', name='example.com')[0]
        
        # Create a mock SocialApp for Microsoft to prevent the SocialApp.DoesNotExist error
        SocialApp.objects.get_or_create(
            provider='microsoft',
            name='Microsoft',
            client_id='dummy-client-id',
            secret='dummy-secret'
        )[0].sites.add(site)
        
        self.client = Client()
        # URL patterns match project structure without namespaces
        self.login_url = reverse('login')
        self.signup_url = reverse('sign_up')
        self.logout_url = reverse('logout')
        
        # Create test users
        self.basic_user = User.objects.create_user(
            username='testbasic',
            email='basic@example.com',
            password='testpassword123',
            role='basic'
        )
        
        self.staff_user = User.objects.create_user(
            username='naim_m',
            email='staff@example.com',
            password='Iambasic',
            role='staff'
        )
        
        self.admin_user = User.objects.create_user(
            username='iamadmin34',
            email='admin@example.com',
            password='admin123#124)',
            role='admin'
        )
    
    def test_login_view_get(self):
        """Test login page loads correctly"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_login_with_valid_credentials(self):
        """Test login with valid credentials redirects to role-based home"""
        # Test basic user
        response = self.client.post(self.login_url, {
            'username': 'testbasic',
            'password': 'testpassword123',
        }, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, '/basic/', fetch_redirect_response=False)
        
        # Logout
        self.client.get(self.logout_url)
        
        # Test staff user
        response = self.client.post(self.login_url, {
            'username': 'naim_m',
            'password': 'Iambasic',
        }, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, '/staff/', fetch_redirect_response=False)
        
        # Logout
        self.client.get(self.logout_url)
        
        # Test admin user
        response = self.client.post(self.login_url, {
            'username': 'iamadmin34',
            'password': 'admin123#124)',
        }, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, '/admin/', fetch_redirect_response=False)
    
    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials shows error"""
        response = self.client.post(self.login_url, {
            'username': 'testbasic',
            'password': 'wrongpassword',
        })
        self.assertFalse(response.context['user'].is_authenticated)
    
    def test_signup_view_get(self):
        """Test signup page loads correctly"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/sign_up.html')
    
    def test_signup_post_valid_data(self):
        """Test valid signup creates new user with basic role"""
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }, follow=True)
        
        # Check user was created
        self.assertEqual(User.objects.count(), 4)  # 3 from setUp + 1 new
        new_user = User.objects.get(username='newuser')
        self.assertTrue(new_user)
        
        # Check role was set to basic
        self.assertEqual(new_user.role, 'basic')
        
        # Check user was authenticated
        self.assertTrue(response.context['user'].is_authenticated)
        
        # Check redirect to basic home
        self.assertRedirects(response, '/basic/', fetch_redirect_response=False)
    
    def test_logout(self):
        """Test user can log out"""
        # First login
        self.client.login(username='testbasic', password='testpassword123')
        # Then logout
        response = self.client.get(self.logout_url, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        # Check redirect to login page
        self.assertRedirects(response, '/accounts/login/', fetch_redirect_response=False)

class AdminPagesTest(TestCase):
    """Test access to admin pages based on user role"""
    
    def setUp(self):
        # Set up test site
        site = Site.objects.get_or_create(domain='example.com', name='example.com')[0]
        
        # Create a mock SocialApp
        SocialApp.objects.get_or_create(
            provider='microsoft',
            name='Microsoft',
            client_id='dummy-client-id',
            secret='dummy-secret'
        )[0].sites.add(site)
        
        self.client = Client()
        
        # Create test users with different roles
        self.basic_user = User.objects.create_user(
            username='testbasic',
            email='basic@example.com',
            password='testpassword123',
            role='basic'
        )
        
        self.staff_user = User.objects.create_user(
            username='naim_m',
            email='staff@example.com',
            password='Iambasic',
            role='staff'
        )
        
        self.admin_user = User.objects.create_user(
            username='iamadmin34',
            email='admin@example.com',
            password='admin123#124)',
            role='admin'
        )
        
        # URLs for admin pages
        self.admin_users_url = reverse('admin_users')
        self.staff_users_url = reverse('staff_users')
    
    def test_basic_user_access_restrictions(self):
        """Test basic users can't access admin/staff pages"""
        self.client.login(username='testbasic', password='testpassword123')
        
        # Try to access admin users page
        response = self.client.get(self.admin_users_url)
        self.assertEqual(response.status_code, 302)  # Redirects away
        
        # Try to access staff users page
        response = self.client.get(self.staff_users_url)
        self.assertEqual(response.status_code, 302)  # Redirects away
    
    def test_staff_user_access(self):
        """Test staff can access staff pages but not admin pages"""
        self.client.login(username='naim_m', password='Iambasic')
        
        # Staff users can access staff users page
        response = self.client.get(self.staff_users_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/staff_users.html')
    
    def test_admin_user_access(self):
        """Test admin can access both admin and staff pages"""
        self.client.login(username='iamadmin34', password='admin123#124)')
        
        # Admin users can access admin users page
        response = self.client.get(self.admin_users_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/admin_users.html')
        
        # Admin users can access staff users page
        response = self.client.get(self.staff_users_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/admin_users.html')

class AdminFeaturesTest(TestCase):
    def setUp(self):
        # Set up test site
        site = Site.objects.get_or_create(domain='example.com', name='example.com')[0]
        
        # Create a mock SocialApp
        SocialApp.objects.get_or_create(
            provider='microsoft',
            name='Microsoft',
            client_id='dummy-client-id',
            secret='dummy-secret'
        )[0].sites.add(site)
        
        self.client = Client()
        
        # Create a test admin user
        self.admin_user = User.objects.create_user(
            username='iamadmin34',
            email='admin@example.com',
            password='admin123#124)',
            role='admin'
        )
        
        # Create a target user for admin actions
        self.target_user = User.objects.create_user(
            username='targetuser',
            email='target@example.com',
            password='targetpass123',
            role='basic'
        )
        
        # URLs for admin actions
        self.change_role_url = reverse('change_role', args=[self.target_user.id])
        self.deactivate_user_url = reverse('deactivate_user', args=[self.target_user.id])
        self.delete_user_url = reverse('delete_user', args=[self.target_user.id])
    
    def test_change_role(self):
        """Test admin can change user roles"""
        self.client.login(username='iamadmin34', password='admin123#124)')
        
        # Change target user role to staff
        response = self.client.post(self.change_role_url, {'new_role': 'staff'}, follow=True)
        
        # Check role was changed
        self.target_user.refresh_from_db()
        self.assertEqual(self.target_user.role, 'staff')
        
        # Check redirect to admin users page
        self.assertRedirects(response, '/accounts/admin/users/', fetch_redirect_response=False)
    
    def test_deactivate_user(self):
        """Test admin can deactivate users"""
        self.client.login(username='iamadmin34', password='admin123#124)')
        
        # Deactivate target user
        response = self.client.post(self.deactivate_user_url, follow=True)
        
        # Check user was deactivated
        self.target_user.refresh_from_db()
        self.assertFalse(self.target_user.is_active)
        
        # Check redirect to admin users page
        self.assertRedirects(response, '/accounts/admin/users/', fetch_redirect_response=False)
    
    def test_delete_user(self):
        """Test admin can delete users"""
        self.client.login(username='iamadmin34', password='admin123#124)')
        
        # Delete target user
        response = self.client.post(self.delete_user_url, follow=True)
        
        # Check user was deleted
        self.assertEqual(User.objects.filter(username='targetuser').count(), 0)
        
        # Check redirect to admin users page
        self.assertRedirects(response, '/accounts/admin/users/', fetch_redirect_response=False)
