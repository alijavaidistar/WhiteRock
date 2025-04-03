document.addEventListener("DOMContentLoaded", function () {
    const statusFilter = document.getElementById("statusFilter");
    const actionFilter = document.getElementById("actionFilter");
    const rows = document.querySelectorAll(".request-row");

    function filterTable() {
        const selectedStatus = statusFilter.value;
        const selectedAction = actionFilter.value;

        rows.forEach(row => {
            const rowStatus = row.dataset.status;
            const rowAction = row.dataset.action;

            const matchesStatus = selectedStatus === "all" || rowStatus === selectedStatus;
            const matchesAction = selectedAction === "all" || rowAction === selectedAction;

            row.style.display = matchesStatus && matchesAction ? "" : "none";
        });
    }

    statusFilter.addEventListener("change", filterTable);
    actionFilter.addEventListener("change", filterTable);
});
