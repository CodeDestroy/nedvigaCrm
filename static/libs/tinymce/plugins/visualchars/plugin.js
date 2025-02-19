/**
 * TinyMCE version 6.4.2 (2023-04-26)
 */
(function () {
    'use strict';
    const Cell = initial => {
        let value = initial;
        const get = () => { return value; }, set = v => { value = v; };
        return {get, set};
    };
    let global = tinymce.util.Tools.resolve('tinymce.PluginManager');
    const get$2 = toggleState => {
        const isEnabled = () => { return toggleState.get(); };
        return {isEnabled};
    };
    const fireVisualChars = (editor, state) => { return editor.dispatch('VisualChars', {state}); };
    const hasProto = (v, constructor, predicate) => {
        let _a;
        if (predicate(v, constructor.prototype)) return true;
        return ((_a = v.constructor) === null || _a === void 0 ? void 0 : _a.name) === constructor.name;
    };
    const typeOf = x => {
        if (x === null) return 'null';
        else if (typeof x === 'object' && Array.isArray(x)) return 'array';
        else if (typeof x === 'object' && hasProto(x, String, (o, proto) => proto.isPrototypeOf(o))) return 'string';
        return typeof x;
    };
    const isType$1 = type => value => typeOf(value) === type, isSimpleType = type => value => typeof value === type;
    const eq = t => a => t === a, isString = isType$1('string'), isObject = isType$1('object'), isNull = eq(null);
    const isBoolean = isSimpleType('boolean'), isNullable = a => a === null || a === undefined;
    const isNonNullable = a => !isNullable(a), isNumber = isSimpleType('number');
    class Optional {
        constructor(tag, value) {
            this.tag = tag;
            this.value = value;
        }
        static some(value) { return new Optional(true, value); }
        static none() { return Optional.singletonNone; }
        fold(onNone, onSome) {
            if (this.tag) return onSome(this.value);
            return onNone();
        }
        isSome() { return this.tag; }
        isNone() { return !this.tag; }
        map(mapper) {
            if (this.tag) return Optional.some(mapper(this.value));
            return Optional.none();
        }
        bind(binder) {
            if (this.tag) return binder(this.value);
            return Optional.none();
        }
        exists(predicate) { return this.tag && predicate(this.value); }
        forall(predicate) { return !this.tag || predicate(this.value); }
        filter(predicate) {
            if (!this.tag || predicate(this.value)) return this;
            return Optional.none();
        }
        getOr(replacement) { return this.tag ? this.value : replacement; }
        or(replacement) { return this.tag ? this : replacement; }
        getOrThunk(thunk) { return this.tag ? this.value : thunk(); }
        orThunk(thunk) { return this.tag ? this : thunk(); }
        getOrDie(message) {
            if (!this.tag) throw new Error(message !== null && message !== void 0 ? message : 'Called getOrDie on None');
            return this.value;
        }
        static from(value) { return isNonNullable(value) ? Optional.some(value) : Optional.none(); }
        getOrNull() { return this.tag ? this.value : null; }
        getOrUndefined() { return this.value; }
        each(worker) {
            if (this.tag) worker(this.value);
        }
        toArray() { return this.tag ? [this.value] : []; }
        toString() { return this.tag ? `some(${this.value})` : 'none()'; }
    }
    Optional.singletonNone = new Optional(false);
    const map = (xs, f) => {
        const r = new Array(xs.length);
        for (let i = 0; i < xs.length; i++) {
            r[i] = f(xs[i], i);
        }
        return r;
    };
    const each$1 = (xs, f) => {
        for (let i = 0, len = xs.length; i < len; i++) {
            const x = xs[i];
            f(x, i);
        }
    };
    const filter = (xs, pred) => {
        const r = [];
        for (let i = 0; i < xs.length; i++) {
            if (pred(xs[i], i)) r.push(xs[i]);
        }
        return r;
    };
    const keys = Object.keys;
    const each = (obj, f) => {
        for (let k = 0; k < keys(obj).length; k++) {
            f(obj[keys(obj)[k]], keys(obj)[k]);
        }
    };
    const Global = typeof window !== 'undefined' ? window : Function('return this;')();
    const path = (parts, scope) => {
        let o = scope !== undefined && scope !== null ? scope : Global;
        for (let i = 0; i < parts.length && o !== undefined && o !== null; ++i) {
            o = o[parts[i]];
        }
        return o;
    };
    const resolve = (p, scope) => { return path(p.split('.'), scope); };
    const unsafe = (name, scope) => { return resolve(name, scope); };
    const getOrDie = (name, scope) => {
        const actual = unsafe(name, scope);
        if (actual === undefined || actual === null) throw new Error(name + ' not available on this browser');
        return actual;
    };
    const getPrototypeOf = Object.getPrototypeOf;
    const sandHTMLElement = scope => { return getOrDie('HTMLElement', scope); };
    const isPrototypeOf = x => {
        return isObject(x) && (sandHTMLElement(resolve('ownerDocument.defaultView', x)).prototype.isPrototypeOf(x) || /^HTML\w*Element$/.test(getPrototypeOf(x).constructor.name));
    };
    const ELEMENT = 1, TEXT = 3, type = element => element.dom.nodeType;
    const value = element => element.dom.nodeValue, isType = t => element => type(element) === t;
    const isHTMLElement = element => isElement(element) && isPrototypeOf(element.dom);
    const isElement = isType(ELEMENT), isText = isType(TEXT);
    const rawSet = (dom, key, value) => {
        if (isString(value) || isBoolean(value) || isNumber(value)) dom.setAttribute(key, value + '');
        else {
            console.error('Invalid call to Attribute.set. Key ', key, ':: Value ', value, ':: Element ', dom);
            throw new Error('Attribute value was not simple');
        }
    };
    const set = (element, key, value) => { rawSet(element.dom, key, value); };
    const get$1 = (element, key) => { return element.dom.getAttribute(key) === null ? undefined : element.dom.getAttribute(key); };
    const remove$3 = (element, key) => { element.dom.removeAttribute(key); };
    const read = (element, attr) => { return get$1(element, attr) === undefined || get$1(element, attr) === '' ? [] : get$1(element, attr).split(' '); };
    const add$2 = (element, attr, id) => {
        set(element, attr, read(element, attr).concat([id]).join(' '));
        return true;
    };
    const remove$2 = (element, attr, id) => {
        if (filter(read(element, attr), v => v !== id).length > 0) set(element, attr, filter(read(element, attr), v => v !== id).join(' '));
        else remove$3(element, attr);
        return false;
    };
    const supports = element => element.dom.classList !== undefined, get = element => read(element, 'class');
    const add$1 = (element, clazz) => add$2(element, 'class', clazz);
    const remove$1 = (element, clazz) => remove$2(element, 'class', clazz);
    const add = (element, clazz) => {
        if (supports(element)) element.dom.classList.add(clazz);
        else add$1(element, clazz);
    };
    const cleanClass = element => {
        const classList = supports(element) ? element.dom.classList : get(element);
        if (classList.length === 0) remove$3(element, 'class');
    };
    const remove = (element, clazz) => {
        if (supports(element)) element.dom.classList.remove(clazz);
        else remove$1(element, clazz);
        cleanClass(element);
    };
    const fromHtml = (html, scope) => {
        const div = (scope || document).createElement('div');
        div.innerHTML = html;
        if (!div.hasChildNodes() || div.childNodes.length > 1) {
            console.error('HTML does not have a single root node', html);
            throw new Error('HTML does not have a single root node');
        }
        return fromDom(div.childNodes[0]);
    };
    const fromTag = (tag, scope) => { return fromDom((scope || document).createElement(tag)); };
    const fromText = (text, scope) => { return fromDom((scope || document).createTextNode(text)); };
    const fromDom = node => {
        if (node === null || node === undefined) throw new Error('Node cannot be null or undefined');
        return {dom: node};
    };
    const fromPoint = (docElm, x, y) => Optional.from(docElm.dom.elementFromPoint(x, y)).map(fromDom);
    const SugarElement = {fromHtml, fromTag, fromText, fromDom, fromPoint};
    const charMap = {'\xA0': 'nbsp', '\xAD': 'shy'};
    const charMapToRegExp = (charMap, global) => {
        let regExp = '';
        each(charMap, (_value, key) => {
            regExp += key;
        });
        return new RegExp('[' + regExp + ']', global ? 'g' : '');
    };
    const charMapToSelector = charMap => {
        let selector = '';
        each(charMap, value => {
            if (selector) selector += ',';
            selector += 'span.mce-' + value;
        });
        return selector;
    };
    const regExp = charMapToRegExp(charMap), regExpGlobal = charMapToRegExp(charMap, true);
    const selector = charMapToSelector(charMap), nbspClass = 'mce-nbsp';
    const getRaw = element => element.dom.contentEditable;
    const wrapCharWithSpan = value => '<span data-mce-bogus="1" class="mce-' + charMap[value] + '">' + value + '</span>';
    const isWrappedNbsp = node => node.nodeName.toLowerCase() === 'span' && node.classList.contains('mce-nbsp-wrap');
    const isMatch = n => { return isText(n) && isString(value(n)) && regExp.test(value(n)); };
    const isContentEditableFalse = node => isHTMLElement(node) && getRaw(node) === 'false';
    const isChildEditable = (node, currentState) => {
        if (isHTMLElement(node) && !isWrappedNbsp(node.dom)) {
            const value = getRaw(node);
            if (value === 'true') return true;
            else if (value === 'false') return false;
        }
        return currentState;
    };
    const filterEditableDescendants = (scope, predicate, editable) => {
        let result = [];
        const children = map(scope.dom.childNodes, SugarElement.fromDom);
        const isEditable = node => isWrappedNbsp(node.dom) || !isContentEditableFalse(node);
        each$1(children, x => {
            if (editable && isEditable(x) && predicate(x)) result = result.concat([x]);
            result = result.concat(filterEditableDescendants(x, predicate, isChildEditable(x, editable)));
        });
        return result;
    };
    const findParentElm = (elm, rootElm) => {
        while (elm.parentNode) {
            if (elm.parentNode === rootElm) return rootElm;
            elm = elm.parentNode;
        }
        return undefined;
    };
    const replaceWithSpans = text => text.replace(regExpGlobal, wrapCharWithSpan);
    const show = (editor, rootElm) => {
        const nodeList = filterEditableDescendants(SugarElement.fromDom(rootElm), isMatch, editor.dom.isEditable(rootElm));
        each$1(nodeList, n => {
            let _a;
            const parent = n.dom.parentNode;
            if (isWrappedNbsp(parent)) add(SugarElement.fromDom(parent), nbspClass);
            else {
                const withSpans = replaceWithSpans(editor.dom.encode((_a = value(n)) !== null && _a !== void 0 ? _a : ''));
                const div = editor.dom.create('div', {}, withSpans);
                let node;
                while (node = div.lastChild) {
                    editor.dom.insertAfter(node, n.dom);
                }
                editor.dom.remove(n.dom);
            }
        });
    };
    const hide = (editor, rootElm) => {
        each$1(editor.dom.select(selector, rootElm), node => {
            if (isWrappedNbsp(node)) remove(SugarElement.fromDom(node), nbspClass);
            else editor.dom.remove(node, true);
        });
    };
    const toggle = editor => {
        let parentNode = findParentElm(editor.selection.getNode(), editor.getBody());
        parentNode = parentNode !== undefined ? parentNode : editor.getBody();
        hide(editor, parentNode);
        show(editor, parentNode);
        editor.selection.moveToBookmark(editor.selection.getBookmark());
    };
    const applyVisualChars = (editor, toggleState) => {
        fireVisualChars(editor, toggleState.get());
        if (toggleState.get() === true) show(editor, editor.getBody());
        else hide(editor, editor.getBody());
    };
    const toggleVisualChars = (editor, toggleState) => {
        toggleState.set(!toggleState.get());
        applyVisualChars(editor, toggleState);
        editor.selection.moveToBookmark(editor.selection.getBookmark());
    };
    const register$2 = (editor, toggleState) => { editor.addCommand('mceVisualChars', () => { toggleVisualChars(editor, toggleState); }); };
    const option = name => editor => editor.options.get(name);
    const register$1 = editor => { editor.options.register('visualchars_default_state', {processor: 'boolean', default: false}); };
    const isEnabledByDefault = option('visualchars_default_state');
    const setup$1 = (editor, toggleState) => { editor.on('init', () => { applyVisualChars(editor, toggleState); }); };
    const first = (fn, rate) => {
        let timer = null;
        const cancel = () => {
            if (!isNull(timer)) {
                clearTimeout(timer);
                timer = null;
            }
        };
        const throttle = (...args) => {
            if (isNull(timer)) {
                timer = setTimeout(() => {
                    timer = null;
                    fn.apply(null, args);
                }, rate);
            }
        };
        return {cancel, throttle};
    };
    const setup = (editor, toggleState) => {
        const debouncedToggle = first(() => {toggle(editor);}, 300);
        editor.on('keydown', e => {
            if (toggleState.get() === true) e.keyCode === 13 ? toggle(editor) : debouncedToggle.throttle();
        });
        editor.on('remove', debouncedToggle.cancel);
    };
    const toggleActiveState = (editor, enabledStated) => api => {
        api.setActive(enabledStated.get());
        const editorEventCallback = e => api.setActive(e.state);
        editor.on('VisualChars', editorEventCallback);
        return () => editor.off('VisualChars', editorEventCallback);
    };
    const register = (editor, toggleState) => {
        const onAction = () => editor.execCommand('mceVisualChars');
        editor.ui.registry.addToggleButton('visualchars', {tooltip: 'Show invisible characters', icon: 'visualchars', onAction, onSetup: toggleActiveState(editor, toggleState)});
        editor.ui.registry.addToggleMenuItem('visualchars', {text: 'Show invisible characters', icon: 'visualchars', onAction, onSetup: toggleActiveState(editor, toggleState)});
    };
    let Plugin = () => {
        global.add('visualchars', editor => {
            register$1(editor);
            const toggleState = Cell(isEnabledByDefault(editor));
            register$2(editor, toggleState);
            register(editor, toggleState);
            setup(editor, toggleState);
            setup$1(editor, toggleState);
            return get$2(toggleState);
        });
    };
    Plugin();
})();