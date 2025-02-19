// make sure requestAnimationFrame and cancelAnimationFrame are defined
// polyfill for browsers without native support
// by Opera engineer Erik Möller
(function () {
    let lastTime = 0, vendors = ['webkit', 'moz', 'ms', 'o'];
    for (let x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[x] + 'RequestAnimationFrame'];
        window.cancelAnimationFrame = window[vendors[x] + 'CancelAnimationFrame'] || window[vendors[x] + 'CancelRequestAnimationFrame'];
    }
    if (!window.requestAnimationFrame) {
        window.requestAnimationFrame = function (callback) {
            let currTime = new Date().getTime(), timeToCall = Math.max(0, 16 - (currTime - lastTime));
            let id = window.setTimeout(function () {
                return callback(currTime + timeToCall);
            }, timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };
    }
    if (!window.cancelAnimationFrame) window.cancelAnimationFrame = function (id) { clearTimeout(id); };
})();