/**
 * TinyMCE version 6.4.2 (2023-04-26)
 */
(function () {
    'use strict';
    let global$1 = tinymce.util.Tools.resolve('tinymce.PluginManager');
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
    const isType = type => value => typeOf(value) === type, isSimpleType = type => value => typeof value === type;
    const isString = isType('string'), isBoolean = isSimpleType('boolean');
    const isNullable = a => a === null || a === undefined, isNonNullable = a => !isNullable(a);
    const isFunction = isSimpleType('function'), option = name => editor => editor.options.get(name);
    const register = editor => {
        const registerOption = editor.options.register;
        const toolbarProcessor = defaultValue => value => {
            const valid = isBoolean(value) || isString(value);
            if (valid) {
                if (isBoolean(value)) return {value: value ? defaultValue : '', valid};
                return {value: value.trim(), valid};
            }
            return {valid: false, message: 'Must be a boolean or string.'};
        };
        const defaultSelectionToolbar = 'bold italic | quicklink h2 h3 blockquote';
        registerOption('quickbars_selection_toolbar', {processor: toolbarProcessor(defaultSelectionToolbar), default: defaultSelectionToolbar});
        const defaultInsertToolbar = 'quickimage quicktable';
        registerOption('quickbars_insert_toolbar', {processor: toolbarProcessor(defaultInsertToolbar), default: defaultInsertToolbar});
        const defaultImageToolbar = 'alignleft aligncenter alignright';
        registerOption('quickbars_image_toolbar', {processor: toolbarProcessor(defaultImageToolbar), default: defaultImageToolbar});
    };
    const getTextSelectionToolbarItems = option('quickbars_selection_toolbar');
    const getInsertToolbarItems = option('quickbars_insert_toolbar');
    const getImageToolbarItems = option('quickbars_image_toolbar');
    let unique = 0;
    const generate = prefix => {
        const time = new Date().getTime(), random = Math.floor(Math.random() * 1000000000);
        unique++;
        return prefix + '_' + random + unique + String(time);
    };
    const insertTable = (editor, columns, rows) => { editor.execCommand('mceInsertTable', false, {rows, columns}); };
    const insertBlob = (editor, base64, blob) => {
        const blobCache = editor.editorUpload.blobCache, blobInfo = blobCache.create(generate('mceu'), blob, base64);
        blobCache.add(blobInfo);
        editor.insertContent(editor.dom.createHTML('img', {src: blobInfo.blobUri()}));
    };
    const blobToBase64 = blob => {
        return new Promise(resolve => {
            const reader = new FileReader();
            reader.onloadend = () => {
                resolve(reader.result.split(',')[1]);
            };
            reader.readAsDataURL(blob);
        });
    };
    let global = tinymce.util.Tools.resolve('tinymce.util.Delay');
    const pickFile = editor => new Promise(resolve => {
        let resolved = false;
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.style.position = 'fixed';
        fileInput.style.left = '0';
        fileInput.style.top = '0';
        fileInput.style.opacity = '0.001';
        document.body.appendChild(fileInput);
        const resolveFileInput = value => {
            let _a;
            if (!resolved) {
                (_a = fileInput.parentNode) === null || _a === void 0 ? void 0 : _a.removeChild(fileInput);
                resolved = true;
                resolve(value);
            }
        };
        const changeHandler = e => { resolveFileInput(Array.prototype.slice.call(e.target.files)); };
        fileInput.addEventListener('input', changeHandler);
        fileInput.addEventListener('change', changeHandler);
        const cancelHandler = e => {
            const cleanup = () => { resolveFileInput([]); };
            if (!resolved) {
                if (e.type === 'focusin') global.setEditorTimeout(editor, cleanup, 1000);
                else cleanup();
            }
            editor.off('focusin remove', cancelHandler);
        };
        editor.on('focusin remove', cancelHandler);
        fileInput.click();
    });
    const setupButtons = editor => {
        editor.ui.registry.addButton('quickimage', {
            icon: 'image',
            tooltip: 'Insert image',
            onAction: () => {
                pickFile(editor).then(files => {
                    if (files.length > 0) blobToBase64(files[0]).then(base64 => { insertBlob(editor, base64, files[0]); });
                });
            }
        });
        editor.ui.registry.addButton('quicktable', {icon: 'table', tooltip: 'Insert table', onAction: () => { insertTable(editor, 2, 2); }});
    };
    const constant = value => { return () => { return value; }; }, never = constant(false);
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
    typeof window !== 'undefined' ? window : Function('return this;')();
    const ELEMENT = 1, name = element => { return element.dom.nodeName.toLowerCase(); };
    const has = (element, key) => { return element.dom && element.dom.hasAttribute ? element.dom.hasAttribute(key) : false; };
    let ClosestOrAncestor = (is, ancestor, scope, a, isRoot) => {
        if (is(scope, a)) return Optional.some(scope);
        else if (isFunction(isRoot) && isRoot(scope)) return Optional.none();
        return ancestor(scope, a, isRoot);
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
    const is = (element, selector) => {
        if (element.dom.nodeType !== ELEMENT) return false;
        else {
            if (element.dom.matches !== undefined) return element.dom.matches(selector);
            else if (element.dom.msMatchesSelector !== undefined) return element.dom.msMatchesSelector(selector);
            else if (element.dom.webkitMatchesSelector !== undefined) return element.dom.webkitMatchesSelector(selector);
            else if (element.dom.mozMatchesSelector !== undefined) return element.dom.mozMatchesSelector(selector);
            throw new Error('Browser lacks native selectors');
        }
    };
    const ancestor$1 = (scope, predicate, isRoot) => {
        let element = scope.dom;
        const stop = isFunction(isRoot) ? isRoot : never;
        while (element.parentNode) {
            element = element.parentNode;
            const el = SugarElement.fromDom(element);
            if (predicate(el)) return Optional.some(el);
            else if (stop(el)) break;
        }
        return Optional.none();
    };
    const closest$2 = (scope, predicate, isRoot) => { return ClosestOrAncestor((s, test) => test(s), ancestor$1, scope, predicate, isRoot); };
    const closest$1 = (scope, predicate, isRoot) => closest$2(scope, predicate, isRoot).isSome();
    const ancestor = (scope, selector, isRoot) => ancestor$1(scope, e => is(e, selector), isRoot);
    const closest = (scope, selector, isRoot) => {
        const is$1 = (element, selector) => is(element, selector);
        return ClosestOrAncestor(is$1, ancestor, scope, selector, isRoot);
    };
    const addToEditor$1 = editor => {
        const insertToolbarItems = getInsertToolbarItems(editor);
        if (insertToolbarItems.length > 0) {
            editor.ui.registry.addContextToolbar('quickblock', {
                predicate: node => {
                    const sugarNode = SugarElement.fromDom(node);
                    const textBlockElementsMap = editor.schema.getTextBlockElements();
                    const isRoot = elem => elem.dom === editor.getBody();
                    return !has(sugarNode, 'data-mce-bogus') && closest(sugarNode, 'table,[data-mce-bogus="all"]', isRoot).fold(() => closest$1(sugarNode, elem => name(elem) in textBlockElementsMap && editor.dom.isEmpty(elem.dom), isRoot), never);
                },
                items: insertToolbarItems,
                position: 'line',
                scope: 'editor'
            });
        }
    };
    const addToEditor = editor => {
        const isEditable = node => editor.dom.getContentEditableParent(node) !== 'false';
        const isImage = node => node.nodeName === 'IMG' || node.nodeName === 'FIGURE' && /image/i.test(node.className);
        const imageToolbarItems = getImageToolbarItems(editor);
        if (imageToolbarItems.length > 0) editor.ui.registry.addContextToolbar('imageselection', {predicate: isImage, items: imageToolbarItems, position: 'node'});
        const textToolbarItems = getTextSelectionToolbarItems(editor);
        if (textToolbarItems.length > 0) {
            editor.ui.registry.addContextToolbar('textselection', {
                predicate: node => !isImage(node) && !editor.selection.isCollapsed() && isEditable(node),
                items: textToolbarItems,
                position: 'selection',
                scope: 'editor'
            });
        }
    };
    let Plugin = () => {
        global$1.add('quickbars', editor => {
            register(editor);
            setupButtons(editor);
            addToEditor$1(editor);
            addToEditor(editor);
        });
    };
    Plugin();
})();