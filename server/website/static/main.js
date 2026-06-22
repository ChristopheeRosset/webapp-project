document.querySelectorAll('.editable-field').forEach(input => {
    input.addEventListener('click', function() {
        this.removeAttribute('readonly');
        this.focus();
    });

    input.addEventListener('blur', function() {
        this.setAttribute('readonly', true);
    });
});