(function (factory) {
    typeof define === 'function' && define.amd ? define(factory) : factory();
})((function () {
    'use strict';
    const calls = new WebSocket('wss://crm.квартиры36.рф/ws/calls/');
    let element = document.getElementById('offcanvasCalls'),
        backdrop = document.querySelector('.offcanvas-backdrop');
    element.querySelector('.close').addEventListener('click', () => {
        element.classList.remove('fade', 'show');
        backdrop.classList.remove('fade', 'show');
        backdrop.classList.add('d-none');
    });
    backdrop.addEventListener('click', () => {
        element.classList.remove('fade', 'show');
        backdrop.classList.remove('fade', 'show');
        backdrop.classList.add('d-none');
    });
    calls.onopen = function () {
        console.log('Call websocket is open');
    };
    calls.onmessage = function (event) {
        try {
            const data = JSON.parse(event.data);
            let callName = element.querySelector('.call-name'), callLink = element.querySelector('.call-link');
            if (typeof (callName) !== 'undefined' && callName !== null) {
                callName.innerHTML = `<span class="h2 me-3">${data.name}</span><span class="h3 fw-bold">${data.phone}</span>`
            }
            if (typeof (callLink) !== 'undefined' && callLink !== null) {
                if (data.link === '#') {
                    callLink.innerText = 'Найти контакт';
                    callLink.href = `/lead/?user=&text=${data.phone}`;
                } else {
                    callLink.innerText = 'Карточка звонящего';
                    callLink.href = data.link;
                }
            }
            element.classList.add('fade', 'show');
            backdrop.classList.remove('d-none');
            backdrop.classList.add('fade', 'show');
        } catch (e) {
            console.log('Call websocket Error:', e.message);
        }
    };
    window.onbeforeunload = () => {
        calls.close();
    };
    window.onbeforeunload = () => {
        calls.close();
    };
}));
