function getInputHtml(elem) {
    if (elem.value.length > 2) {
        let request = new XMLHttpRequest(), formData = new FormData();
        if (elem.hasAttribute('data-get')) request.open('GET', elem.dataset.get + '?chars=' + elem.value);
        else request.open('POST', elem.dataset.post);
        request.onloadend = function () {
            if (elem.hasAttribute('data-swap')) {
                let target = document.querySelector(elem.dataset.target);
                if (elem.dataset.swap === 'innerHtml') target.innerHTML = this.responseText;
                else target.outerHTML = this.responseText;
                (target.querySelectorAll('.dropdown-item') || []).forEach(($trigger) => {
                    $trigger.addEventListener('click', () => {
                        let hiddenField = $trigger.closest('.input-group').querySelector('input[type="hidden"]'),
                            nameField = $trigger.closest('.input-group').querySelector('.name');
                        hiddenField.value = $trigger.dataset.id;
                        nameField.value = $trigger.innerText;
                    });
                });
            }
        };
        request.send(formData);
    }
}