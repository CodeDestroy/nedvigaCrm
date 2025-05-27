'use strict';
function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) throw new TypeError("Cannot call a class as a function");
}
function _defineProperties(target, props) {
    for (let i = 0; i < props.length; i++) {
        let descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
    }
}
function _createClass(Constructor, protoProps, staticProps) {
    if (protoProps) _defineProperties(Constructor.prototype, protoProps);
    if (staticProps) _defineProperties(Constructor, staticProps);
    return Constructor;
}
let defaults = {
    classNames: {active: 'gl-active', base: 'gl-star-rating', selected: 'gl-selected'},
    clearable: true,
    maxStars: 10,
    prebuilt: false,
    stars: null,
    tooltip: 'Select a Rating'
};
let addRemoveClass = function addRemoveClass(el, bool, className) { el.classList[bool ? 'add' : 'remove'](className); };
let createSpanEl = function createSpanEl(attributes) {
    let el = document.createElement('span');
    attributes = attributes || {};
    for (let key in attributes) {
        el.setAttribute(key, attributes[key]);
    }
    return el;
};
let inRange = function inRange(value, min, max) { return /^\d+$/.test(value) && min <= value && value <= max; };
let insertSpanEl = function insertSpanEl(el, after, attributes) {
    let newEl = createSpanEl(attributes);
    el.parentNode.insertBefore(newEl, after ? el.nextSibling : el);
    return newEl;
};
let merge = function merge() {
    for (let _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
        args[_key] = arguments[_key];
    }
    // adapted from https://github.com/firstandthird/aug
    let results = {};
    args.forEach(function (prop) {
        Object.keys(prop || {}).forEach(function (propName) {
            if (args[0][propName] === undefined) return; // restrict keys to the defaults
            let propValue = prop[propName];
            if (type(propValue) === 'Object' && type(results[propName]) === 'Object') {
                results[propName] = merge(results[propName], propValue);
                return;
            }
            results[propName] = propValue;
        });
    });
    return results;
};
let type = function type(value) { return {}.toString.call(value).slice(8, -1); };
let values = function values(selectEl) {
    let values = [];
    [].forEach.call(selectEl.options, function (el) {
        let value = parseInt(el.value, 10) || 0;
        if (value > 0) values.push({index: el.index, text: el.text, value: value});
    });
    return values.sort(function (a, b) { return a.value - b.value; });
};
let Widget = /*#__PURE__*/function () {
    function Widget(el, props) {
        _classCallCheck(this, Widget);
        // (HTMLElement, object):void
        this.direction = window.getComputedStyle(el, null).getPropertyValue('direction');
        this.el = el;
        this.events = {
            change: this.onChange.bind(this),
            keydown: this.onKeyDown.bind(this),
            mousedown: this.onPointerDown.bind(this),
            mouseleave: this.onPointerLeave.bind(this),
            mousemove: this.onPointerMove.bind(this),
            reset: this.onReset.bind(this),
            touchend: this.onPointerDown.bind(this),
            touchmove: this.onPointerMove.bind(this)
        };
        this.indexActive = null; // the active span index
        this.indexSelected = null; // the selected span index
        this.props = props;
        this.tick = null;
        this.ticking = false;
        this.values = values(el);
        this.widgetEl = null;
        if (this.el.widget) this.el.widget.destroy(); // remove any stale event listeners
        if (inRange(this.values.length, 1, this.props.maxStars)) this.build();
        else this.destroy();
    }
    _createClass(Widget, [{
        key: "build",
        value: function build() {
            // ():void
            this.destroy();
            this.buildWidget();
            this.selectValue(this.indexSelected = this.selected(), false); // set the initial value but do not trigger change event
            this.handleEvents('add');
            this.el.widget = this; // store a reference to this widget on the SELECT so that we can remove stale event listeners
        }
    }, {
        key: "buildWidget",
        value: function buildWidget() {
            let _this = this;
            // ():void
            let parentEl, widgetEl;
            if (this.props.prebuilt) {
                parentEl = this.el.parentNode;
                widgetEl = parentEl.querySelector('.' + this.props.classNames.base + '--stars');
            } else {
                parentEl = insertSpanEl(this.el, false, {"class": this.props.classNames.base});
                parentEl.appendChild(this.el);
                widgetEl = insertSpanEl(this.el, true, {"class": this.props.classNames.base + '--stars'});
                this.values.forEach(function (item, index) {
                    let el = createSpanEl({'data-index': index, 'data-value': item.value});
                    if ('function' === typeof _this.props.stars) _this.props.stars.call(_this, el, item, index);
                    [].forEach.call(el.children, function (el) { return el.style.pointerEvents = 'none'; });
                    widgetEl.innerHTML += el.outerHTML;
                });
            }
            parentEl.dataset.starRating = '';
            parentEl.classList.add(this.props.classNames.base + '--' + this.direction);
            if (this.props.tooltip) widgetEl.setAttribute('role', 'tooltip');
            this.widgetEl = widgetEl;
        }
    }, {
        key: "changeIndexTo",
        value: function changeIndexTo(index, force) {
            let _this2 = this;
            // (int):void
            if (this.indexActive !== index || force) {
                [].forEach.call(this.widgetEl.children, function (el, i) {
                    // i starts at zero
                    addRemoveClass(el, i <= index, _this2.props.classNames.active);
                    addRemoveClass(el, i === _this2.indexSelected, _this2.props.classNames.selected);
                });
                this.widgetEl.setAttribute('data-rating', index + 1);
                if ('function' !== typeof this.props.stars && !this.props.prebuilt) {
                    // @v3 compat
                    this.widgetEl.classList.remove('s' + 10 * (this.indexActive + 1));
                    this.widgetEl.classList.add('s' + 10 * (index + 1));
                }
                if (this.props.tooltip) {
                    let _this$values$index;
                    let label = index < 0 ? this.props.tooltip : (_this$values$index = this.values[index]) === null || _this$values$index === void 0 ? void 0 : _this$values$index.text;
                    this.widgetEl.setAttribute('aria-label', label);
                }
                this.indexActive = index;
            }
            this.ticking = false;
        }
    }, {
        key: "destroy",
        value: function destroy() {
            // ():void
            this.indexActive = null; // the active span index
            this.indexSelected = this.selected(); // the selected span index
            let parentEl = this.el.parentNode;
            if (parentEl.classList.contains(this.props.classNames.base)) {
                if (this.props.prebuilt) {
                    this.widgetEl = parentEl.querySelector('.' + this.props.classNames.base + '--stars');
                    parentEl.classList.remove(this.props.classNames.base + '--' + this.direction);
                    delete parentEl.dataset.starRating;
                } else parentEl.parentNode.replaceChild(this.el, parentEl);
                this.handleEvents('remove');
            }
            delete this.el.widget; // remove the widget reference
        }
    }, {
        key: "eventListener",
        value: function eventListener(el, action, events, items) {
            let _this3 = this;
            // (HTMLElement, string, array, object):void
            events.forEach(function (ev) { return el[action + 'EventListener'](ev, _this3.events[ev], items || false); });
        }
    }, {
        key: "handleEvents",
        value: function handleEvents(action) {
            // (string):void
            let formEl = this.el.closest('form');
            if (formEl && formEl.tagName === 'FORM') this.eventListener(formEl, action, ['reset']);
            this.eventListener(this.el, action, ['change']); // always trigger the change event, even when SELECT is disabled
            if ('add' === action && this.el.disabled) return;
            this.eventListener(this.el, action, ['keydown']);
            this.eventListener(this.widgetEl, action, ['mousedown', 'mouseleave', 'mousemove', 'touchend', 'touchmove'], false);
        }
    }, {
        key: "indexFromEvent",
        value: function indexFromEvent(ev) {
            let _ev$touches, _ev$changedTouches;
            // (MouseEvent|TouchEvent):void
            let origin = ((_ev$touches = ev.touches) === null || _ev$touches === void 0 ? void 0 : _ev$touches[0]) || ((_ev$changedTouches = ev.changedTouches) === null || _ev$changedTouches === void 0 ? void 0 : _ev$changedTouches[0]) || ev;
            let el = document.elementFromPoint(origin.clientX, origin.clientY);
            if (el.parentNode === this.widgetEl) return [].slice.call(el.parentNode.children).indexOf(el);
            return this.indexActive;
        }
    }, {
        key: "onChange",
        value: function onChange() { this.changeIndexTo(this.selected(), true); }
    }, {
        key: "onKeyDown",
        value: function onKeyDown(ev) {
            // (KeyboardEvent):void
            let key = ev.key.slice(5);
            if (!~['Left', 'Right'].indexOf(key)) return;
            ev.preventDefault();
            let increment = key === 'Left' ? -1 : 1;
            if (this.direction === 'rtl') increment *= -1;
            let maxIndex = this.values.length - 1, minIndex = -1;
            let index = Math.min(Math.max(this.selected() + increment, minIndex), maxIndex);
            this.selectValue(index, true); // trigger change event
        }
    }, {
        key: "onPointerDown",
        value: function onPointerDown(ev) {
            // (MouseEvent|TouchEvent):void
            ev.preventDefault(); // this.el.focus(); // highlight the rating field
            let index = this.indexFromEvent(ev);
            if (this.props.clearable && index === this.indexSelected) index = -1; // remove the value
            this.selectValue(index, true); // trigger change event
        }
    }, {
        key: "onPointerLeave",
        value: function onPointerLeave(ev) {
            let _this4 = this;
            // (MouseEvent):void
            ev.preventDefault();
            cancelAnimationFrame(this.tick);
            requestAnimationFrame(function () { return _this4.changeIndexTo(_this4.indexSelected); });
        }
    }, {
        key: "onPointerMove",
        value: function onPointerMove(ev) {
            let _this5 = this;
            // (MouseEvent|TouchEvent):void
            ev.preventDefault();
            if (!this.ticking) {
                this.tick = requestAnimationFrame(function () { return _this5.changeIndexTo(_this5.indexFromEvent(ev)); });
                this.ticking = true;
            }
        }
    }, {
        key: "onReset",
        value: function onReset() {
            let _this$el$querySelecto;
            // ():void
            let index = this.valueIndex((_this$el$querySelecto = this.el.querySelector('[selected]')) === null || _this$el$querySelecto === void 0 ? void 0 : _this$el$querySelecto.value);
            this.selectValue(index || -1, false); // do not trigger change event
        }
    }, {
        key: "selected",
        value: function selected() { return this.valueIndex(this.el.value); }
    }, {
        key: "selectValue",
        value: function selectValue(index, triggerChangeEvent) {
            let _this$values$index2;
            // (int, bool):void
            this.el.value = ((_this$values$index2 = this.values[index]) === null || _this$values$index2 === void 0 ? void 0 : _this$values$index2.value) || ''; // first set the new value
            this.indexSelected = this.selected(); // get the actual index from the selected value
            if (false === triggerChangeEvent) this.changeIndexTo(this.selected(), true);
            else this.el.dispatchEvent(new Event('change'));
        }
    }, {
        key: "valueIndex",
        value: function valueIndex(value) { return this.values.findIndex(function (val) { return val.value === +value; }); }
    }]);
    return Widget;
}();
let StarRating = /*#__PURE__*/function () {
    function StarRating(selector, props) {
        _classCallCheck(this, StarRating);
        // (HTMLSelectElement|NodeList|string, object):void
        this.destroy = this.destroy.bind(this);
        this.props = props;
        this.rebuild = this.rebuild.bind(this);
        this.selector = selector;
        this.widgets = [];
        this.build();
    }
    _createClass(StarRating, [{
        key: "build",
        value: function build() {
            let _this = this;
            // (HTMLSelectElement|NodeList|string, object):void
            this.queryElements(this.selector).forEach(function (el) {
                let options = merge(defaults, _this.props, JSON.parse(el.getAttribute('data-options')));
                if ('SELECT' === el.tagName && !el.widget) {
                    // check for an existing Widget reference
                    if (!options.prebuilt && el.parentNode.classList.contains(options.classNames.base)) _this.unwrap(el);
                    _this.widgets.push(new Widget(el, options));
                }
            });
        }
    }, {
        key: "destroy",
        value: function destroy() {
            // ():void
            this.widgets.forEach(function (widget) { return widget.destroy(); });
            this.widgets = [];
        }
    }, {
        key: "queryElements",
        value: function queryElements(selector) {
            // (HTMLSelectElement|NodeList|string):array
            if ('HTMLSelectElement' === type(selector)) return [selector];
            if ('NodeList' === type(selector)) return [].slice.call(selector);
            if ('String' === type(selector)) return [].slice.call(document.querySelectorAll(selector));
            return [];
        }
    }, {
        key: "rebuild",
        value: function rebuild() {
            // ():void
            this.destroy();
            this.build();
        }
    }, {
        key: "unwrap",
        value: function unwrap(el) {
            let removeEl = el.parentNode, parentEl = removeEl.parentNode;
            parentEl.insertBefore(el, removeEl);
            parentEl.removeChild(removeEl);
        }
    }]);
    return StarRating;
}();
module.exports = StarRating;