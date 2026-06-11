// ===============================
// Delete Confirmation
// ===============================

function confirmDelete() {

    return confirm(
        "Are you sure you want to delete this expense?"
    );

}

// ===============================
// Delete All Confirmation
// ===============================

function confirmDeleteAll() {

    return confirm(
        "This will delete ALL expense records.\n\nContinue?"
    );

}

// ===============================
// Search Validation
// ===============================

function validateSearch() {

    const query =
        document.getElementById("searchInput").value;

    if (query.trim() === "") {

        alert("Please enter a search term.");

        return false;
    }

    return true;
}

// ===============================
// Auto Hide Alerts
// ===============================

setTimeout(() => {

    const alerts =
        document.querySelectorAll(".alert");

    alerts.forEach(alert => {

        alert.style.transition = "0.5s";

        alert.style.opacity = "0";

        setTimeout(() => {

            alert.remove();

        }, 500);

    });

}, 3000);

// ===============================
// Table Row Highlight
// ===============================

document.addEventListener("DOMContentLoaded", () => {

    const rows =
        document.querySelectorAll("tbody tr");

    rows.forEach(row => {

        row.addEventListener("click", () => {

            rows.forEach(r =>
                r.classList.remove("table-active")
            );

            row.classList.add("table-active");

        });

    });

});