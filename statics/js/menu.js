function checkAll(allCheckbox) {
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name="category"]');
    checkboxes.forEach(chk => {
        if (chk !== allCheckbox) {
            chk.checked = false;
        }
    });
}

function uncheckCategoryAll() {
    document.getElementById("all").checked = false;
}