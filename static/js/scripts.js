(() => {
    'use strict';
    // ==============================================================
    // Auto select left navbar
    // ==============================================================
    let $horizontalNav = document.querySelectorAll('#navbar-menu a'), $flag = false;
    for (let i = $horizontalNav.length - 1; i > -1; i--) {
        if (!$flag) {
            let re = new RegExp($horizontalNav[i].href);
            if (re.test(window.location.href)) {
                $flag = true;
                $horizontalNav[i].parentElement.classList.add('active');
            }
        }
    }
})();

function getHtml(elem) {
    if (elem.hasAttribute('data-swap')) {
        document.querySelector(elem.dataset.target).innerHTML = '<video width="200" height="200" autoplay loop class="mx-auto my-5 d-block"><source src="/static/img/loading.webm" type="video/webm" /></video>'
    }
    let request = new XMLHttpRequest(), formData = new FormData();
    if (elem.hasAttribute('data-get')) request.open('GET', elem.dataset.get);
    else request.open('POST', elem.dataset.post);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    request.onloadend = function () {
        // TODO: если немного докинуть свойств, то можно будет получить полную замену htmx в +- 30 строк
        if (elem.hasAttribute('data-swap')) {
            if (elem.dataset.swap === 'innerHtml') document.querySelector(elem.dataset.target).innerHTML = this.responseText;
            else document.querySelector(elem.dataset.target).outerHTML = this.responseText
        }
    };
    request.send(formData);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}