(() => {
    'use strict'
    const btn = document.getElementById('clients');
    btn.addEventListener('click', async () => {
        let form = btn.closest('form'), formData = new FormData(form),
            request = new XMLHttpRequest();
        request.open('POST', '/reports/lead/');
        request.onloadend = function () {
            const response = JSON.parse(this.responseText);
            console.log(response.message);
            return true;
        };
        formData.append('csrfmiddlewaretoken', JSON.parse(document.body.getAttribute('hx-headers'))['X-CSRFToken']);
        request.send(formData);
    });
})();