/**
 * TinyMCE version 6.4.2 (2023-04-26)
 */
(function () {
    'use strict';
    let global$7 = tinymce.util.Tools.resolve('tinymce.PluginManager');
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
    const isString = isType$1('string'), isObject = isType$1('object');
    const isArray = isType$1('array'), isBoolean = isSimpleType('boolean');
    const isNullable = a => a === null || a === undefined, isNonNullable = a => !isNullable(a);
    const isFunction = isSimpleType('function'), isNumber = isSimpleType('number');
    const noop = () => {};
    const constant = value => { return () => { return value; }; };
    const tripleEquals = (a, b) => { return a === b; };
    const not = f => t => !f(t), never = constant(false);
    class Optional {
        constructor(tag, value) {
            this.tag = tag;
            this.value = value;
        }

        static some(value) {
            return new Optional(true, value);
        }
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
    const nativeSlice = Array.prototype.slice, nativeIndexOf = Array.prototype.indexOf;
    const nativePush = Array.prototype.push, rawIndexOf = (ts, t) => nativeIndexOf.call(ts, t);
    const contains$1 = (xs, x) => rawIndexOf(xs, x) > -1;
    const exists = (xs, pred) => {
        for (let i = 0; i < xs.length; i++) {
            if (pred(xs[i], i)) return true;
        }
        return false;
    };
    const map = (xs, f) => {
        const r = new Array(xs.length);
        for (let i = 0; i < xs.length; i++) {
            r[i] = f(xs[i], i);
        }
        return r;
    };
    const each$1 = (xs, f) => {
        for (let i = 0, len = xs.length; i < len; i++) {
            f(xs[i], i);
        }
    };
    const filter$1 = (xs, pred) => {
        const r = [];
        for (let i = 0, len = xs.length; i < len; i++) {
            if (pred(xs[i], i)) r.push(xs[i]);
        }
        return r;
    };
    const groupBy = (xs, f) => {
        if (xs.length === 0) return [];
        let wasType = f(xs[0]);
        const r = [];
        let group = [];
        for (let i = 0, len = xs.length; i < len; i++) {
            if (f(xs[i]) !== wasType) {
                r.push(group);
                group = [];
            }
            wasType = f(xs[i]);
            group.push(xs[i]);
        }
        if (group.length !== 0) r.push(group);
        return r;
    };
    const foldl = (xs, f, acc) => {
        each$1(xs, (x, i) => {
            acc = f(acc, x, i);
        });
        return acc;
    };
    const findUntil = (xs, pred, until) => {
        for (let i = 0, len = xs.length; i < len; i++) {
            if (pred(xs[i], i)) return Optional.some(xs[i]);
            else if (until(xs[i], i)) break;
        }
        return Optional.none();
    };
    const find = (xs, pred) => { return findUntil(xs, pred, never); };
    const flatten = xs => {
        const r = [];
        for (let i = 0, len = xs.length; i < len; ++i) {
            if (!isArray(xs[i])) throw new Error('Arr.flatten item ' + i + ' was not an array, input: ' + xs);
            nativePush.apply(r, xs[i]);
        }
        return r;
    };
    const bind = (xs, f) => flatten(map(xs, f));
    const reverse = xs => {
        const r = nativeSlice.call(xs, 0);
        r.reverse();
        return r;
    };
    const get$1 = (xs, i) => i >= 0 && i < xs.length ? Optional.some(xs[i]) : Optional.none();
    const head = xs => get$1(xs, 0), last = xs => get$1(xs, xs.length - 1);
    const unique = (xs, comparator) => {
        const r = [];
        const isDuplicated = isFunction(comparator) ? x => exists(r, i => comparator(i, x)) : x => contains$1(r, x);
        for (let i = 0; i < xs.length; i++) {
            if (!isDuplicated(xs[i])) r.push(xs[i]);
        }
        return r;
    };
    const is$2 = (lhs, rhs, comparator = tripleEquals) => lhs.exists(left => comparator(left, rhs));
    const equals = (lhs, rhs, comparator = tripleEquals) => lift2(lhs, rhs, comparator).getOr(lhs.isNone() && rhs.isNone());
    const lift2 = (oa, ob, f) => oa.isSome() && ob.isSome() ? Optional.some(f(oa.getOrDie(), ob.getOrDie())) : Optional.none();
    const ELEMENT = 1;
    const fromHtml = (html, scope) => {
        const div = (scope || document).createElement('div');
        div.innerHTML = html;
        if (!div.hasChildNodes() || div.childNodes.length > 1) {
            console.error('HTML does not have a single root node', html);
            throw new Error('HTML does not have a single root node');
        }
        return fromDom$1(div.childNodes[0]);
    };
    const fromTag = (tag, scope) => { return fromDom$1((scope || document).createElement(tag)); };
    const fromText = (text, scope) => { return fromDom$1((scope || document).createTextNode(text)); };
    const fromDom$1 = node => {
        if (node === null || node === undefined) throw new Error('Node cannot be null or undefined');
        return {dom: node};
    };
    const fromPoint = (docElm, x, y) => Optional.from(docElm.dom.elementFromPoint(x, y)).map(fromDom$1);
    const SugarElement = {fromHtml, fromTag, fromText, fromDom: fromDom$1, fromPoint};
    const is$1 = (element, selector) => {
        if (element.dom.nodeType !== ELEMENT) return false;
        const elem = element.dom;
        if (elem.matches !== undefined) return elem.matches(selector);
        else if (elem.msMatchesSelector !== undefined) return elem.msMatchesSelector(selector);
        else if (elem.webkitMatchesSelector !== undefined) return elem.webkitMatchesSelector(selector);
        else if (elem.mozMatchesSelector !== undefined) return elem.mozMatchesSelector(selector);
        throw new Error('Browser lacks native selectors');
    };
    const eq = (e1, e2) => e1.dom === e2.dom;
    const contains = (e1, e2) => { return e1.dom === e2.dom ? false : e1.dom.contains(e2.dom); };
    const is = is$1;
    let ClosestOrAncestor = (is, ancestor, scope, a, isRoot) => {
        if (is(scope, a)) return Optional.some(scope);
        else if (isFunction(isRoot) && isRoot(scope)) return Optional.none();
        return ancestor(scope, a, isRoot);
    };
    typeof window !== 'undefined' ? window : Function('return this;')();
    const name = element => { return element.dom.nodeName.toLowerCase(); };
    const type = element => element.dom.nodeType, isType = t => element => type(element) === t;
    const isElement$1 = isType(ELEMENT), isTag = tag => e => isElement$1(e) && name(e) === tag;
    const parent = element => Optional.from(element.dom.parentNode).map(SugarElement.fromDom);
    const parentElement = element => Optional.from(element.dom.parentElement).map(SugarElement.fromDom);
    const nextSibling = element => Optional.from(element.dom.nextSibling).map(SugarElement.fromDom);
    const children = element => map(element.dom.childNodes, SugarElement.fromDom);
    const child = (element, index) => { return Optional.from(element.dom.childNodes[index]).map(SugarElement.fromDom); };
    const firstChild = element => child(element, 0);
    const lastChild = element => child(element, element.dom.childNodes.length - 1);
    const ancestor = (scope, predicate, isRoot) => {
        let element = scope.dom;
        const stop = isFunction(isRoot) ? isRoot : never;
        while (element.parentNode) {
            element = element.parentNode;
            if (predicate(SugarElement.fromDom(element))) return Optional.some(SugarElement.fromDom(element));
            else if (stop(SugarElement.fromDom(element))) break;
        }
        return Optional.none();
    };
    const closest = (scope, predicate, isRoot) => {
        const is = (s, test) => test(s);
        return ClosestOrAncestor(is, ancestor, scope, predicate, isRoot);
    };
    const before$1 = (marker, element) => {
        const parent$1 = parent(marker);
        parent$1.each(v => { v.dom.insertBefore(element.dom, marker.dom); });
    };
    const after = (marker, element) => {
        const sibling = nextSibling(marker);
        sibling.fold(() => {
            const parent$1 = parent(marker);
            parent$1.each(v => { append$1(v, element); });
        }, v => { before$1(v, element); });
    };
    const append$1 = (parent, element) => { parent.dom.appendChild(element.dom); };
    const before = (marker, elements) => { each$1(elements, x => { before$1(marker, x); }); };
    const append = (parent, elements) => { each$1(elements, x => { append$1(parent, x); }); };
    const empty = element => {
        element.dom.textContent = '';
        each$1(children(element), rogue => { remove(rogue); });
    };
    const remove = element => {
        if (element.dom.parentNode !== null) element.dom.parentNode.removeChild(element.dom);
    };
    let global$6 = tinymce.util.Tools.resolve('tinymce.dom.RangeUtils');
    let global$5 = tinymce.util.Tools.resolve('tinymce.dom.TreeWalker');
    let global$4 = tinymce.util.Tools.resolve('tinymce.util.VK');
    const fromDom = nodes => map(nodes, SugarElement.fromDom), keys = Object.keys;
    const each = (obj, f) => {
        for (let k = 0; k < keys(obj).length; k++) {
            f(obj[keys(obj)[k]], keys(obj)[k]);
        }
    };
    const objAcc = r => (x, i) => {
        r[i] = x;
    };
    const internalFilter = (obj, pred, onTrue, onFalse) => {
        each(obj, (x, i) => { (pred(x, i) ? onTrue : onFalse)(x, i); });
    };
    const filter = (obj, pred) => {
        const t = {};
        internalFilter(obj, pred, objAcc(t), noop);
        return t;
    };
    const rawSet = (dom, key, value) => {
        if (isString(value) || isBoolean(value) || isNumber(value)) dom.setAttribute(key, value + '');
        else {
            console.error('Invalid call to Attribute.set. Key ', key, ':: Value ', value, ':: Element ', dom);
            throw new Error('Attribute value was not simple');
        }
    };
    const setAll = (element, attrs) => { each(attrs, (v, k) => { rawSet(element.dom, k, v); }); };
    const clone$1 = element => foldl(element.dom.attributes, (acc, attr) => {
        acc[attr.name] = attr.value;
        return acc;
    }, {});
    const clone = (original, isDeep) => SugarElement.fromDom(original.dom.cloneNode(isDeep));
    const deep = original => clone(original, true);
    const shallowAs = (original, tag) => {
        setAll(SugarElement.fromTag(tag), clone$1(original));
        return SugarElement.fromTag(tag);
    };
    const mutate = (original, tag) => {
        after(original, shallowAs(original, tag));
        append(shallowAs(original, tag), children(original));
        remove(original);
        return shallowAs(original, tag);
    };
    let global$3 = tinymce.util.Tools.resolve('tinymce.dom.DOMUtils');
    let global$2 = tinymce.util.Tools.resolve('tinymce.util.Tools');
    const matchNodeName = name => node => isNonNullable(node) && node.nodeName.toLowerCase() === name;
    const matchNodeNames = regex => node => isNonNullable(node) && regex.test(node.nodeName);
    const isTextNode$1 = node => isNonNullable(node) && node.nodeType === 3;
    const isElement = node => isNonNullable(node) && node.nodeType === 1;
    const isListNode = matchNodeNames(/^(OL|UL|DL)$/), isOlUlNode = matchNodeNames(/^(OL|UL)$/);
    const isOlNode = matchNodeName('ol'), isListItemNode = matchNodeNames(/^(LI|DT|DD)$/);
    const isDlItemNode = matchNodeNames(/^(DT|DD)$/), isTableCellNode = matchNodeNames(/^(TH|TD)$/);
    const isBr = matchNodeName('br');
    const isFirstChild = node => {
        let _a;
        return ((_a = node.parentNode) === null || _a === void 0 ? void 0 : _a.firstChild) === node;
    };
    const isTextBlock = (editor, node) => isNonNullable(node) && node.nodeName in editor.schema.getTextBlockElements();
    const isBlock = (node, blockElements) => isNonNullable(node) && node.nodeName in blockElements;
    const isVoid = (editor, node) => isNonNullable(node) && node.nodeName in editor.schema.getVoidElements();
    const isBogusBr = (dom, node) => {
        if (!isBr(node)) return false;
        return dom.isBlock(node.nextSibling) && !isBr(node.previousSibling);
    };
    const isEmpty$2 = (dom, elm, keepBookmarks) => {
        if (keepBookmarks && dom.select('span[data-mce-type=bookmark]', elm).length > 0) return false;
        return dom.isEmpty(elm);
    };
    const isChildOfBody = (dom, elm) => dom.isChildOf(elm, dom.getRoot()), option = name => editor => editor.options.get(name);
    const register$3 = editor => { editor.options.register('lists_indent_on_tab', {processor: 'boolean', default: true}); };
    const shouldIndentOnTab = option('lists_indent_on_tab');
    const getForcedRootBlock = option('forced_root_block');
    const getForcedRootBlockAttrs = option('forced_root_block_attrs');
    const createTextBlock = (editor, contentNode) => {
        const blockElements = editor.schema.getBlockElements();
        const fragment = editor.dom.createFragment();
        const blockName = getForcedRootBlock(editor);
        const blockAttrs = getForcedRootBlockAttrs(editor);
        let node, textBlock, hasContentNode = false;
        textBlock = editor.dom.create(blockName, blockAttrs);
        if (!isBlock(contentNode.firstChild, blockElements)) fragment.appendChild(textBlock);
        while (node = contentNode.firstChild) {
            const nodeName = node.nodeName;
            if (!hasContentNode && (nodeName !== 'SPAN' || node.getAttribute('data-mce-type') !== 'bookmark')) hasContentNode = true;
            if (isBlock(node, blockElements)) {
                fragment.appendChild(node);
                textBlock = null;
            } else {
                if (!textBlock) {
                    textBlock = editor.dom.create(blockName, blockAttrs);
                    fragment.appendChild(textBlock);
                }
                textBlock.appendChild(node);
            }
        }
        if (!hasContentNode && textBlock) textBlock.appendChild(editor.dom.create('br', {'data-mce-bogus': '1'}));
        return fragment;
    };
    const DOM$2 = global$3.DOM;
    const splitList = (editor, list, li) => {
        const removeAndKeepBookmarks = targetNode => {
            const parent = targetNode.parentNode;
            if (parent) global$2.each(bookmarks, node => { parent.insertBefore(node, li.parentNode); });
            DOM$2.remove(targetNode);
        };
        const bookmarks = DOM$2.select('span[data-mce-type="bookmark"]', list);
        const newBlock = createTextBlock(editor, li), tmpRng = DOM$2.createRng();
        tmpRng.setStartAfter(li);
        tmpRng.setEndAfter(list);
        const fragment = tmpRng.extractContents();
        for (let node = fragment.firstChild; node; node = node.firstChild) {
            if (node.nodeName === 'LI' && editor.dom.isEmpty(node)) {
                DOM$2.remove(node);
                break;
            }
        }
        if (!editor.dom.isEmpty(fragment)) DOM$2.insertAfter(fragment, list);
        DOM$2.insertAfter(newBlock, list);
        if (li.parentElement && isEmpty$2(editor.dom, li.parentElement)) removeAndKeepBookmarks(li.parentElement);
        DOM$2.remove(li);
        if (isEmpty$2(editor.dom, list)) DOM$2.remove(list);
    };
    const isDescriptionDetail = isTag('dd'), isDescriptionTerm = isTag('dt');
    const outdentDlItem = (editor, item) => {
        if (isDescriptionDetail(item)) mutate(item, 'dt');
        else if (isDescriptionTerm(item)) parentElement(item).each(dl => splitList(editor, dl.dom, item.dom));
    };
    const indentDlItem = item => {
        if (isDescriptionTerm(item)) mutate(item, 'dd');
    };
    const dlIndentation = (editor, indentation, dlItems) => {
        if (indentation === 'Indent') each$1(dlItems, indentDlItem);
        else each$1(dlItems, item => outdentDlItem(editor, item));
    };
    const getNormalizedPoint = (container, offset) => {
        if (isTextNode$1(container)) return {container, offset};
        const node = global$6.getNode(container, offset);
        if (isTextNode$1(node)) return {container: node, offset: offset >= container.childNodes.length ? node.data.length : 0};
        else if (node.previousSibling && isTextNode$1(node.previousSibling)) return {container: node.previousSibling, offset: node.previousSibling.data.length};
        else if (node.nextSibling && isTextNode$1(node.nextSibling)) return {container: node.nextSibling, offset: 0};
        return {container, offset};
    };
    const normalizeRange = rng => {
        const outRng = rng.cloneRange(), rangeStart = getNormalizedPoint(rng.startContainer, rng.startOffset);
        outRng.setStart(rangeStart.container, rangeStart.offset);
        const rangeEnd = getNormalizedPoint(rng.endContainer, rng.endOffset);
        outRng.setEnd(rangeEnd.container, rangeEnd.offset);
        return outRng;
    };
    const listNames = ['OL', 'UL', 'DL'], listSelector = listNames.join(',');
    const getParentList = (editor, node) => {
        const selectionStart = node || editor.selection.getStart(true);
        return editor.dom.getParent(selectionStart, listSelector, getClosestListHost(editor, selectionStart));
    };
    const isParentListSelected = (parentList, selectedBlocks) => isNonNullable(parentList) && selectedBlocks.length === 1 && selectedBlocks[0] === parentList;
    const findSubLists = parentList => filter$1(parentList.querySelectorAll(listSelector), isListNode);
    const getSelectedSubLists = editor => {
        const parentList = getParentList(editor), selectedBlocks = editor.selection.getSelectedBlocks();
        if (isParentListSelected(parentList, selectedBlocks)) return findSubLists(parentList);
        return filter$1(selectedBlocks, elm => { return isListNode(elm) && parentList !== elm; });
    };
    const findParentListItemsNodes = (editor, elms) => {
        const listItemsElms = global$2.map(elms, elm => {
            const parentLi = editor.dom.getParent(elm, 'li,dd,dt', getClosestListHost(editor, elm));
            return parentLi ? parentLi : elm;
        });
        return unique(listItemsElms);
    };
    const getSelectedListItems = editor => { return filter$1(findParentListItemsNodes(editor, editor.selection.getSelectedBlocks()), isListItemNode); };
    const getSelectedDlItems = editor => filter$1(getSelectedListItems(editor), isDlItemNode);
    const getClosestEditingHost = (editor, elm) => {
        const parentTableCell = editor.dom.getParents(elm, 'TD,TH');
        return parentTableCell.length > 0 ? parentTableCell[0] : editor.getBody();
    };
    const isListHost = (schema, node) => !isListNode(node) && !isListItemNode(node) && exists(listNames, listName => schema.isValidChild(node.nodeName, listName));
    const getClosestListHost = (editor, elm) => {
        const parentBlock = find(editor.dom.getParents(elm, editor.dom.isBlock), elm => isListHost(editor.schema, elm));
        return parentBlock.getOr(editor.getBody());
    };
    const findLastParentListNode = (editor, elm) => {
        return last(editor.dom.getParents(elm, 'ol,ul', getClosestListHost(editor, elm)));
    };
    const getSelectedLists = editor => {
        const firstList = findLastParentListNode(editor, editor.selection.getStart());
        const subsequentLists = filter$1(editor.selection.getSelectedBlocks(), isOlUlNode);
        return firstList.toArray().concat(subsequentLists);
    };
    const getSelectedListRoots = editor => { return getUniqueListRoots(editor, getSelectedLists(editor)); };
    const getUniqueListRoots = (editor, lists) => { return unique(map(lists, list => findLastParentListNode(editor, list).getOr(list))); };
    const isCustomList = list => /\btox\-/.test(list.className);
    const inList = (parents, listName) => findUntil(parents, isListNode, isTableCellNode).exists(list => list.nodeName === listName && !isCustomList(list));
    const isWithinNonEditable = (editor, element) => element !== null && !editor.dom.isEditable(element);
    const selectionIsWithinNonEditableList = editor => { return isWithinNonEditable(editor, getParentList(editor)); };
    const isWithinNonEditableList = (editor, element) => { return isWithinNonEditable(editor, editor.dom.getParent(element, 'ol,ul,dl')); };
    const hasNonEditableBlocksSelected = editor => exists(editor.selection.getSelectedBlocks(), not(editor.dom.isEditable));
    const setNodeChangeHandler = (editor, nodeChangeHandler) => {
        nodeChangeHandler({parents: editor.dom.getParents(editor.selection.getNode()), element: editor.selection.getNode()});
        editor.on('NodeChange', nodeChangeHandler);
        return () => editor.off('NodeChange', nodeChangeHandler);
    };
    const fromElements = (elements, scope) => {
        const fragment = (scope || document).createDocumentFragment();
        each$1(elements, element => {
            fragment.appendChild(element.dom);
        });
        return SugarElement.fromDom(fragment);
    };
    const fireListEvent = (editor, action, element) => editor.dispatch('ListMutation', {action, element});
    const blank = r => s => s.replace(r, ''), trim = blank(/^\s+|\s+$/g);
    const isNotEmpty = s => s.length > 0, isEmpty$1 = s => !isNotEmpty(s);
    const isSupported = dom => dom.style !== undefined && isFunction(dom.style.getPropertyValue);
    const internalSet = (dom, property, value) => {
        if (!isString(value)) {
            console.error('Invalid call to CSS.set. Property ', property, ':: Value ', value, ':: Element ', dom);
            throw new Error('CSS value must be a string: ' + value);
        }
        if (isSupported(dom)) dom.style.setProperty(property, value);
    };
    const set = (element, property, value) => { internalSet(element.dom, property, value); };
    const joinSegment = (parent, child) => { append$1(parent.item, child.list); };
    const joinSegments = segments => {
        for (let i = 1; i < segments.length; i++) {
            joinSegment(segments[i - 1], segments[i]);
        }
    };
    const appendSegments = (head$1, tail) => { lift2(last(head$1), head(tail), joinSegment); };
    const createSegment = (scope, listType) => {
        const segment = {list: SugarElement.fromTag(listType, scope), item: SugarElement.fromTag('li', scope)};
        append$1(segment.list, segment.item);
        return segment;
    };
    const createSegments = (scope, entry, size) => {
        const segments = [];
        for (let i = 0; i < size; i++) {
            segments.push(createSegment(scope, entry.listType));
        }
        return segments;
    };
    const populateSegments = (segments, entry) => {
        for (let i = 0; i < segments.length - 1; i++) {
            set(segments[i].item, 'list-style-type', 'none');
        }
        last(segments).each(segment => {
            setAll(segment.list, entry.listAttributes);
            setAll(segment.item, entry.itemAttributes);
            append(segment.item, entry.content);
        });
    };
    const normalizeSegment = (segment, entry) => {
        if (name(segment.list) !== entry.listType) segment.list = mutate(segment.list, entry.listType);
        setAll(segment.list, entry.listAttributes);
    };
    const createItem = (scope, attr, content) => {
        setAll(SugarElement.fromTag('li', scope), attr);
        append(SugarElement.fromTag('li', scope), content);
        return SugarElement.fromTag('li', scope);
    };
    const appendItem = (segment, item) => {
        append$1(segment.list, item);
        segment.item = item;
    };
    const writeShallow = (scope, cast, entry) => {
        last(cast.slice(0, entry.depth)).each(segment => {
            appendItem(segment, createItem(scope, entry.itemAttributes, entry.content));
            normalizeSegment(segment, entry);
        });
        return cast.slice(0, entry.depth);
    };
    const writeDeep = (scope, cast, entry) => {
        const segments = createSegments(scope, entry, entry.depth - cast.length);
        joinSegments(segments);
        populateSegments(segments, entry);
        appendSegments(cast, segments);
        return cast.concat(segments);
    };
    const composeList = (scope, entries) => {
        const cast = foldl(entries, (cast, entry) => {
            return entry.depth > cast.length ? writeDeep(scope, cast, entry) : writeShallow(scope, cast, entry);
        }, []);
        return head(cast).map(segment => segment.list);
    };
    const isList = el => is(el, 'OL,UL'), hasFirstChildList = el => firstChild(el).exists(isList);
    const hasLastChildList = el => lastChild(el).exists(isList);
    const isIndented = entry => entry.depth > 0, isSelected = entry => entry.isSelected;
    const cloneItemContent = li => { return map(hasLastChildList(li) ? children(li).slice(0, -1) : children(li), deep); };
    const createEntry = (li, depth, isSelected) => parent(li).filter(isElement$1).map(list => ({
        depth,
        dirty: false,
        isSelected,
        content: cloneItemContent(li),
        itemAttributes: clone$1(li),
        listAttributes: clone$1(list),
        listType: name(list)
    }));
    const indentEntry = (indentation, entry) => {
        switch (indentation) {
            case 'Indent':
                entry.depth++;
                break;
            case 'Outdent':
                entry.depth--;
                break;
            case 'Flatten':
                entry.depth = 0;
        }
        entry.dirty = true;
    };
    const cloneListProperties = (target, source) => {
        target.listType = source.listType;
        target.listAttributes = {...source.listAttributes};
    };
    const cleanListProperties = entry => {
        entry.listAttributes = filter(entry.listAttributes, (_value, key) => key !== 'start');
    };
    const closestSiblingEntry = (entries, start) => {
        const depth = entries[start].depth, matches = entry => entry.depth === depth && !entry.dirty;
        const until = entry => entry.depth < depth;
        return findUntil(reverse(entries.slice(0, start)), matches, until).orThunk(() => findUntil(entries.slice(start + 1), matches, until));
    };
    const normalizeEntries = entries => {
        each$1(entries, (entry, i) => {
            closestSiblingEntry(entries, i).fold(() => {
                if (entry.dirty) cleanListProperties(entry);
            }, matchingEntry => cloneListProperties(entry, matchingEntry));
        });
        return entries;
    };
    const Cell = initial => {
        let value = initial;
        const get = () => { return value; };
        const set = v => { value = v; };
        return {get, set};
    };
    const parseItem = (depth, itemSelection, selectionState, item) => firstChild(item).filter(isList).fold(() => {
        itemSelection.each(selection => {
            if (eq(selection.start, item)) selectionState.set(true);
        });
        const currentItemEntry = createEntry(item, depth, selectionState.get());
        itemSelection.each(selection => {
            if (eq(selection.end, item)) selectionState.set(false);
        });
        const childListEntries = lastChild(item).filter(isList).map(list => parseList(depth, itemSelection, selectionState, list)).getOr([]);
        return currentItemEntry.toArray().concat(childListEntries);
    }, list => parseList(depth, itemSelection, selectionState, list));
    const parseList = (depth, itemSelection, selectionState, list) => bind(children(list), element => {
        const parser = isList(element) ? parseList : parseItem;
        const newDepth = depth + 1;
        return parser(newDepth, itemSelection, selectionState, element);
    });
    const parseLists = (lists, itemSelection) => {
        return map(lists, list => ({sourceList: list, entries: parseList(0, itemSelection, Cell(false), list)}));
    };
    const outdentedComposer = (editor, entries) => {
        return map(normalizeEntries(entries), entry => {
            return SugarElement.fromDom(createTextBlock(editor, fromElements(entry.content).dom));
        });
    };
    const indentedComposer = (editor, entries) => { return composeList(editor.contentDocument, normalizeEntries(entries)).toArray(); };
    const composeEntries = (editor, entries) => bind(groupBy(entries, isIndented), entries => { return head(entries).exists(isIndented) ? indentedComposer(editor, entries) : outdentedComposer(editor, entries); });
    const indentSelectedEntries = (entries, indentation) => { each$1(filter$1(entries, isSelected), entry => indentEntry(indentation, entry)); };
    const getItemSelection = editor => {
        const selectedListItems = map(getSelectedListItems(editor), SugarElement.fromDom);
        return lift2(find(selectedListItems, not(hasFirstChildList)), find(reverse(selectedListItems), not(hasFirstChildList)), (start, end) => ({
            start,
            end
        }));
    };
    const listIndentation = (editor, lists, indentation) => {
        each$1(parseLists(lists, getItemSelection(editor)), entrySet => {
            indentSelectedEntries(entrySet.entries, indentation);
            each$1(composeEntries(editor, entrySet.entries), composedList => {
                fireListEvent(editor, indentation === 'Indent' ? 'IndentList' : 'OutdentList', composedList.dom);
            });
            before(entrySet.sourceList, composeEntries(editor, entrySet.entries));
            remove(entrySet.sourceList);
        });
    };
    const selectionIndentation = (editor, indentation) => {
        const lists = fromDom(getSelectedListRoots(editor)), dlItems = fromDom(getSelectedDlItems(editor));
        let isHandled = false;
        if (lists.length || dlItems.length) {
            const bookmark = editor.selection.getBookmark();
            listIndentation(editor, lists, indentation);
            dlIndentation(editor, indentation, dlItems);
            editor.selection.moveToBookmark(bookmark);
            editor.selection.setRng(normalizeRange(editor.selection.getRng()));
            editor.nodeChanged();
            isHandled = true;
        }
        return isHandled;
    };
    const handleIndentation = (editor, indentation) => !selectionIsWithinNonEditableList(editor) && selectionIndentation(editor, indentation);
    const indentListSelection = editor => handleIndentation(editor, 'Indent');
    const outdentListSelection = editor => handleIndentation(editor, 'Outdent');
    const flattenListSelection = editor => handleIndentation(editor, 'Flatten');
    const zeroWidth = '\uFEFF', isZwsp = char => char === zeroWidth;
    let global$1 = tinymce.util.Tools.resolve('tinymce.dom.BookmarkManager');
    const DOM$1 = global$3.DOM;
    const createBookmark = rng => {
        const bookmark = {};
        const setupEndPoint = start => {
            let container = rng[start ? 'startContainer' : 'endContainer'], offset = rng[start ? 'startOffset' : 'endOffset'];
            if (isElement(container)) {
                const offsetNode = DOM$1.create('span', {'data-mce-type': 'bookmark'});
                if (container.hasChildNodes()) {
                    offset = Math.min(offset, container.childNodes.length - 1);
                    if (start) container.insertBefore(offsetNode, container.childNodes[offset]);
                    else DOM$1.insertAfter(offsetNode, container.childNodes[offset]);
                } else container.appendChild(offsetNode);
                container = offsetNode;
                offset = 0;
            }
            bookmark[start ? 'startContainer' : 'endContainer'] = container;
            bookmark[start ? 'startOffset' : 'endOffset'] = offset;
        };
        setupEndPoint(true);
        if (!rng.collapsed) setupEndPoint();
        return bookmark;
    };
    const resolveBookmark = bookmark => {
        const restoreEndPoint = start => {
            const nodeIndex = container => {
                let _a;
                let node = (_a = container.parentNode) === null || _a === void 0 ? void 0 : _a.firstChild;
                let idx = 0;
                while (node) {
                    if (node === container) return idx;
                    if (!isElement(node) || node.getAttribute('data-mce-type') !== 'bookmark') idx++;
                    node = node.nextSibling;
                }
                return -1;
            };
            let container = bookmark[start ? 'startContainer' : 'endContainer'];
            let offset = bookmark[start ? 'startOffset' : 'endOffset'];
            if (!container) return;
            if (isElement(container) && container.parentNode) {
                const node = container;
                offset = nodeIndex(container);
                container = container.parentNode;
                DOM$1.remove(node);
                if (!container.hasChildNodes() && DOM$1.isBlock(container)) container.appendChild(DOM$1.create('br'));
            }
            bookmark[start ? 'startContainer' : 'endContainer'] = container;
            bookmark[start ? 'startOffset' : 'endOffset'] = offset;
        };
        restoreEndPoint(true);
        restoreEndPoint();
        const rng = DOM$1.createRng();
        rng.setStart(bookmark.startContainer, bookmark.startOffset);
        if (bookmark.endContainer) rng.setEnd(bookmark.endContainer, bookmark.endOffset);
        return normalizeRange(rng);
    };

    const listToggleActionFromListName = listName => {
        switch (listName) {
            case 'UL':
                return 'ToggleUlList';
            case 'OL':
                return 'ToggleOlList';
            case 'DL':
                return 'ToggleDLList';
        }
    };

    const updateListStyle = (dom, el, detail) => {
        const type = detail['list-style-type'] ? detail['list-style-type'] : null;
        dom.setStyle(el, 'list-style-type', type);
    };
    const setAttribs = (elm, attrs) => {
        global$2.each(attrs, (value, key) => { elm.setAttribute(key, value); });
    };
    const updateListAttrs = (dom, el, detail) => {
        setAttribs(el, detail['list-attributes']);
        global$2.each(dom.select('li', el), li => { setAttribs(li, detail['list-item-attributes']); });
    };
    const updateListWithDetails = (dom, el, detail) => {
        updateListStyle(dom, el, detail);
        updateListAttrs(dom, el, detail);
    };
    const removeStyles = (dom, element, styles) => { global$2.each(styles, style => dom.setStyle(element, style, '')); };
    const isInline = (editor, node) => isNonNullable(node) && !isBlock(node, editor.schema.getBlockElements());
    const getEndPointNode = (editor, rng, start, root) => {
        let container = rng[start ? 'startContainer' : 'endContainer'];
        const offset = rng[start ? 'startOffset' : 'endOffset'];
        if (isElement(container)) container = container.childNodes[Math.min(offset, container.childNodes.length - 1)] || container;
        if (!start && isBr(container.nextSibling)) container = container.nextSibling;
        const findBetterContainer = (container, forward) => {
            let _a;
            const walker = new global$5(container, root), dir = forward ? 'next' : 'prev';
            let node;
            while (node = walker[dir]()) {
                if (!(isVoid(editor, node) || isZwsp(node.textContent) || ((_a = node.textContent) === null || _a === void 0 ? void 0 : _a.length) === 0)) return Optional.some(node);
            }
            return Optional.none();
        };
        if (start && isTextNode$1(container)) {
            if (isZwsp(container.textContent)) container = findBetterContainer(container, false).getOr(container);
            else {
                if (container.parentNode !== null && isInline(editor, container.parentNode)) container = container.parentNode;
                while (container.previousSibling !== null && (isInline(editor, container.previousSibling) || isTextNode$1(container.previousSibling))) {
                    container = container.previousSibling;
                }
            }
        }
        if (!start && isTextNode$1(container)) {
            if (isZwsp(container.textContent)) container = findBetterContainer(container, true).getOr(container);
            else {
                if (container.parentNode !== null && isInline(editor, container.parentNode)) container = container.parentNode;
                while (container.nextSibling !== null && (isInline(editor, container.nextSibling) || isTextNode$1(container.nextSibling))) {
                    container = container.nextSibling;
                }
            }
        }
        while (container.parentNode !== root) {
            const parent = container.parentNode;
            if (isTextBlock(editor, container)) return container;
            if (/^(TD|TH)$/.test(parent.nodeName)) return container;
            container = parent;
        }
        return container;
    };
    const getSelectedTextBlocks = (editor, rng, root) => {
        const textBlocks = [], dom = editor.dom;
        const startNode = getEndPointNode(editor, rng, true, root);
        const endNode = getEndPointNode(editor, rng, false, root);
        let block;
        const siblings = [];
        for (let node = startNode; node; node = node.nextSibling) {
            siblings.push(node);
            if (node === endNode) break;
        }
        global$2.each(siblings, node => {
            let _a;
            if (isTextBlock(editor, node)) {
                textBlocks.push(node);
                block = null;
                return;
            }
            if (dom.isBlock(node) || isBr(node)) {
                if (isBr(node)) dom.remove(node);
                block = null;
                return;
            }
            const nextSibling = node.nextSibling;
            if (global$1.isBookmarkNode(node)) {
                if (isListNode(nextSibling) || isTextBlock(editor, nextSibling) || !nextSibling && node.parentNode === root) {
                    block = null;
                    return;
                }
            }
            if (!block) {
                block = dom.create('p');
                (_a = node.parentNode) === null || _a === void 0 ? void 0 : _a.insertBefore(block, node);
                textBlocks.push(block);
            }
            block.appendChild(node);
        });
        return textBlocks;
    };
    const hasCompatibleStyle = (dom, sib, detail) => {
        const sibStyle = dom.getStyle(sib, 'list-style-type');
        let detailStyle = detail ? detail['list-style-type'] : '';
        detailStyle = detailStyle === null ? '' : detailStyle;
        return sibStyle === detailStyle;
    };
    const applyList = (editor, listName, detail) => {
        const rng = editor.selection.getRng();
        let listItemName = 'LI';
        const root = getClosestListHost(editor, editor.selection.getStart(true)), dom = editor.dom;
        if (dom.getContentEditable(editor.selection.getNode()) === 'false') return;
        listName = listName.toUpperCase();
        if (listName === 'DL') listItemName = 'DT';
        const bookmark = createBookmark(rng), selectedTextBlocks = getSelectedTextBlocks(editor, rng, root);
        global$2.each(selectedTextBlocks, block => {
            let listBlock;
            const sibling = block.previousSibling, parent = block.parentNode;
            if (!isListItemNode(parent)) {
                if (sibling && isListNode(sibling) && sibling.nodeName === listName && hasCompatibleStyle(dom, sibling, detail)) {
                    listBlock = sibling;
                    block = dom.rename(block, listItemName);
                    sibling.appendChild(block);
                } else {
                    listBlock = dom.create(listName);
                    parent.insertBefore(listBlock, block);
                    listBlock.appendChild(block);
                    block = dom.rename(block, listItemName);
                }
                removeStyles(dom, block, ['margin', 'margin-right', 'margin-bottom', 'margin-left', 'margin-top', 'padding', 'padding-right', 'padding-bottom', 'padding-left', 'padding-top']);
                updateListWithDetails(dom, listBlock, detail);
                mergeWithAdjacentLists(editor.dom, listBlock);
            }
        });
        editor.selection.setRng(resolveBookmark(bookmark));
    };
    const isValidLists = (list1, list2) => { return isListNode(list1) && list1.nodeName === (list2 === null || list2 === void 0 ? void 0 : list2.nodeName); };
    const hasSameListStyle = (dom, list1, list2) => {
        const targetStyle = dom.getStyle(list1, 'list-style-type', true), style = dom.getStyle(list2, 'list-style-type', true);
        return targetStyle === style;
    };
    const hasSameClasses = (elm1, elm2) => { return elm1.className === elm2.className; };
    const shouldMerge = (dom, list1, list2) => { return isValidLists(list1, list2) && hasSameListStyle(dom, list1, list2) && hasSameClasses(list1, list2); };
    const mergeWithAdjacentLists = (dom, listBlock) => {
        let node, sibling = listBlock.nextSibling;
        if (shouldMerge(dom, listBlock, sibling)) {
            const liSibling = sibling;
            while (node = liSibling.firstChild) {
                listBlock.appendChild(node);
            }
            dom.remove(liSibling);
        }
        sibling = listBlock.previousSibling;
        if (shouldMerge(dom, listBlock, sibling)) {
            const liSibling = sibling;
            while (node = liSibling.lastChild) {
                listBlock.insertBefore(node, listBlock.firstChild);
            }
            dom.remove(liSibling);
        }
    };
    const updateList$1 = (editor, list, listName, detail) => {
        if (list.nodeName !== listName) {
            const newList = editor.dom.rename(list, listName);
            updateListWithDetails(editor.dom, newList, detail);
            fireListEvent(editor, listToggleActionFromListName(listName), newList);
        } else {
            updateListWithDetails(editor.dom, list, detail);
            fireListEvent(editor, listToggleActionFromListName(listName), list);
        }
    };
    const toggleMultipleLists = (editor, parentList, lists, listName, detail) => {
        const parentIsList = isListNode(parentList);
        if (parentIsList && parentList.nodeName === listName && !hasListStyleDetail(detail)) flattenListSelection(editor);
        else {
            applyList(editor, listName, detail);
            const bookmark = createBookmark(editor.selection.getRng());
            const allLists = parentIsList ? [parentList, ...lists] : lists;
            global$2.each(allLists, elm => { updateList$1(editor, elm, listName, detail); });
            editor.selection.setRng(resolveBookmark(bookmark));
        }
    };
    const hasListStyleDetail = detail => { return 'list-style-type' in detail; };
    const toggleSingleList = (editor, parentList, listName, detail) => {
        if (parentList === editor.getBody()) return;
        if (parentList) {
            if (parentList.nodeName === listName && !hasListStyleDetail(detail) && !isCustomList(parentList)) flattenListSelection(editor);
            else {
                const bookmark = createBookmark(editor.selection.getRng());
                updateListWithDetails(editor.dom, parentList, detail);
                const newList = editor.dom.rename(parentList, listName);
                mergeWithAdjacentLists(editor.dom, newList);
                editor.selection.setRng(resolveBookmark(bookmark));
                applyList(editor, listName, detail);
                fireListEvent(editor, listToggleActionFromListName(listName), newList);
            }
        } else {
            applyList(editor, listName, detail);
            fireListEvent(editor, listToggleActionFromListName(listName), parentList);
        }
    };
    const toggleList = (editor, listName, _detail) => {
        const parentList = getParentList(editor);
        if (isWithinNonEditableList(editor, parentList) || hasNonEditableBlocksSelected(editor)) return;
        const selectedSubLists = getSelectedSubLists(editor), detail = isObject(_detail) ? _detail : {};
        if (selectedSubLists.length > 0) toggleMultipleLists(editor, parentList, selectedSubLists, listName, detail);
        else toggleSingleList(editor, parentList, listName, detail);
    };
    const DOM = global$3.DOM;
    const normalizeList = (dom, list) => {
        const parentNode = list.parentElement;
        if (parentNode && parentNode.nodeName === 'LI' && parentNode.firstChild === list) {
            const sibling = parentNode.previousSibling;
            if (sibling && sibling.nodeName === 'LI') {
                sibling.appendChild(list);
                if (isEmpty$2(dom, parentNode)) DOM.remove(parentNode);
            } else DOM.setStyle(parentNode, 'listStyleType', 'none');
        }
        if (isListNode(parentNode)) {
            const sibling = parentNode.previousSibling;
            if (sibling && sibling.nodeName === 'LI') sibling.appendChild(list);
        }
    };
    const normalizeLists = (dom, element) => {
        const lists = global$2.grep(dom.select('ol,ul', element));
        global$2.each(lists, list => {
            normalizeList(dom, list);
        });
    };

    const findNextCaretContainer = (editor, rng, isForward, root) => {
        let node = rng.startContainer;
        const offset = rng.startOffset;
        if (isTextNode$1(node) && (isForward ? offset < node.data.length : offset > 0)) return node;
        const nonEmptyBlocks = editor.schema.getNonEmptyElements();
        if (isElement(node)) node = global$6.getNode(node, offset);
        const walker = new global$5(node, root);
        if (isForward) {
            if (isBogusBr(editor.dom, node)) walker.next();
        }
        const walkFn = isForward ? walker.next.bind(walker) : walker.prev2.bind(walker);
        while (node = walkFn()) {
            if (node.nodeName === 'LI' && !node.hasChildNodes()) return node;
            if (nonEmptyBlocks[node.nodeName]) return node;
            if (isTextNode$1(node) && node.data.length > 0) return node;
        }
        return null;
    };
    const hasOnlyOneBlockChild = (dom, elm) => {
        const childNodes = elm.childNodes;
        return childNodes.length === 1 && !isListNode(childNodes[0]) && dom.isBlock(childNodes[0]);
    };
    const unwrapSingleBlockChild = (dom, elm) => {
        if (hasOnlyOneBlockChild(dom, elm)) dom.remove(elm.firstChild, true);
    };
    const moveChildren = (dom, fromElm, toElm) => {
        let node;
        const targetElm = hasOnlyOneBlockChild(dom, toElm) ? toElm.firstChild : toElm;
        unwrapSingleBlockChild(dom, fromElm);
        if (!isEmpty$2(dom, fromElm, true)) {
            while (node = fromElm.firstChild) {
                targetElm.appendChild(node);
            }
        }
    };
    const mergeLiElements = (dom, fromElm, toElm) => {
        let listNode;
        const ul = fromElm.parentNode;
        if (!isChildOfBody(dom, fromElm) || !isChildOfBody(dom, toElm)) return;
        if (isListNode(toElm.lastChild)) listNode = toElm.lastChild;
        if (ul === toElm.lastChild) {
            if (isBr(ul.previousSibling)) dom.remove(ul.previousSibling);
        }
        const node = toElm.lastChild;
        if (node && isBr(node) && fromElm.hasChildNodes()) dom.remove(node);
        if (isEmpty$2(dom, toElm, true)) empty(SugarElement.fromDom(toElm));
        moveChildren(dom, fromElm, toElm);
        if (listNode) toElm.appendChild(listNode);
        const contains$1 = contains(SugarElement.fromDom(toElm), SugarElement.fromDom(fromElm));
        const nestedLists = contains$1 ? dom.getParents(fromElm, isListNode, toElm) : [];
        dom.remove(fromElm);
        each$1(nestedLists, list => {
            if (isEmpty$2(dom, list) && list !== dom.getRoot()) dom.remove(list);
        });
    };
    const mergeIntoEmptyLi = (editor, fromLi, toLi) => {
        empty(SugarElement.fromDom(toLi));
        mergeLiElements(editor.dom, fromLi, toLi);
        editor.selection.setCursorLocation(toLi, 0);
    };
    const mergeForward = (editor, rng, fromLi, toLi) => {
        const dom = editor.dom;
        if (dom.isEmpty(toLi)) mergeIntoEmptyLi(editor, fromLi, toLi);
        else {
            const bookmark = createBookmark(rng);
            mergeLiElements(dom, fromLi, toLi);
            editor.selection.setRng(resolveBookmark(bookmark));
        }
    };
    const mergeBackward = (editor, rng, fromLi, toLi) => {
        const bookmark = createBookmark(rng);
        mergeLiElements(editor.dom, fromLi, toLi);
        const resolvedBookmark = resolveBookmark(bookmark);
        editor.selection.setRng(resolvedBookmark);
    };
    const backspaceDeleteFromListToListCaret = (editor, isForward) => {
        const dom = editor.dom, selection = editor.selection, selectionStartElm = selection.getStart();
        const root = getClosestEditingHost(editor, selectionStartElm);
        const li = dom.getParent(selection.getStart(), 'LI', root);
        if (li) {
            const ul = li.parentElement;
            if (ul === editor.getBody() && isEmpty$2(dom, ul)) return true;
            const rng = normalizeRange(selection.getRng());
            const otherLi = dom.getParent(findNextCaretContainer(editor, rng, isForward, root), 'LI', root);
            if (otherLi && otherLi !== li) {
                editor.undoManager.transact(() => {
                    if (isForward) mergeForward(editor, rng, otherLi, li);
                    else {
                        if (isFirstChild(li)) outdentListSelection(editor);
                        else mergeBackward(editor, rng, li, otherLi);
                    }
                });
                return true;
            } else if (!otherLi) {
                if (!isForward && rng.startOffset === 0 && rng.endOffset === 0) {
                    editor.undoManager.transact(() => { flattenListSelection(editor); });
                    return true;
                }
            }
        }
        return false;
    };
    const removeBlock = (dom, block, root) => {
        const parentBlock = dom.getParent(block.parentNode, dom.isBlock, root);
        dom.remove(block);
        if (parentBlock && dom.isEmpty(parentBlock)) dom.remove(parentBlock);
    };
    const backspaceDeleteIntoListCaret = (editor, isForward) => {
        const dom = editor.dom, selectionStartElm = editor.selection.getStart();
        const root = getClosestEditingHost(editor, selectionStartElm);
        const block = dom.getParent(selectionStartElm, dom.isBlock, root);
        if (block && dom.isEmpty(block)) {
            const rng = normalizeRange(editor.selection.getRng());
            const otherLi = dom.getParent(findNextCaretContainer(editor, rng, isForward, root), 'LI', root);
            if (otherLi) {
                const findValidElement = element => contains$1(['td', 'th', 'caption'], name(element));
                const findRoot = node => node.dom === root;
                const otherLiCell = closest(SugarElement.fromDom(otherLi), findValidElement, findRoot);
                const caretCell = closest(SugarElement.fromDom(rng.startContainer), findValidElement, findRoot);
                if (!equals(otherLiCell, caretCell, eq)) return false;
                editor.undoManager.transact(() => {
                    removeBlock(dom, block, root);
                    mergeWithAdjacentLists(dom, otherLi.parentNode);
                    editor.selection.select(otherLi, true);
                    editor.selection.collapse(isForward);
                });
                return true;
            }
        }
        return false;
    };
    const backspaceDeleteCaret = (editor, isForward) => {
        return backspaceDeleteFromListToListCaret(editor, isForward) || backspaceDeleteIntoListCaret(editor, isForward);
    };
    const hasListSelection = editor => {
        const selectionStartElm = editor.selection.getStart();
        const root = getClosestEditingHost(editor, selectionStartElm);
        const startListParent = editor.dom.getParent(selectionStartElm, 'LI,DT,DD', root);
        return startListParent || getSelectedListItems(editor).length > 0;
    };
    const backspaceDeleteRange = editor => {
        if (hasListSelection(editor)) {
            editor.undoManager.transact(() => {
                editor.execCommand('Delete');
                normalizeLists(editor.dom, editor.getBody());
            });
            return true;
        }
        return false;
    };
    const backspaceDelete = (editor, isForward) => { return !isWithinNonEditableList(editor, editor.selection.getNode()) && (editor.selection.isCollapsed() ? backspaceDeleteCaret(editor, isForward) : backspaceDeleteRange(editor)); };
    const setup$2 = editor => {
        editor.on('ExecCommand', e => {
            if ((e.command.toLowerCase() === 'delete' || e.command.toLowerCase() === 'forwarddelete') && hasListSelection(editor)) normalizeLists(editor.dom, editor.getBody());
        });
        editor.on('keydown', e => {
            if (e.keyCode === global$4.BACKSPACE) {
                if (backspaceDelete(editor, false)) e.preventDefault();
            } else if (e.keyCode === global$4.DELETE) {
                if (backspaceDelete(editor, true)) e.preventDefault();
            }
        });
    };
    const get = editor => ({backspaceDelete: isForward => { backspaceDelete(editor, isForward); }});
    const updateList = (editor, update) => {
        const parentList = getParentList(editor);
        if (parentList === null || isWithinNonEditableList(editor, parentList)) return;
        editor.undoManager.transact(() => {
            if (isObject(update.styles)) editor.dom.setStyles(parentList, update.styles);
            if (isObject(update.attrs)) each(update.attrs, (v, k) => editor.dom.setAttrib(parentList, k, v));
        });
    };
    const parseAlphabeticBase26 = str => {
        const chars = reverse(trim(str).split(''));
        const values = map(chars, (char, i) => {
            const charValue = char.toUpperCase().charCodeAt(0) - 'A'.charCodeAt(0) + 1;
            return Math.pow(26, i) * charValue;
        });
        return foldl(values, (sum, v) => sum + v, 0);
    };
    const composeAlphabeticBase26 = value => {
        value--;
        if (value < 0) return '';
        else {
            const remainder = value % 26, quotient = Math.floor(value / 26);
            const rest = composeAlphabeticBase26(quotient), char = String.fromCharCode('A'.charCodeAt(0) + remainder);
            return rest + char;
        }
    };
    const isUppercase = str => /^[A-Z]+$/.test(str), isLowercase = str => /^[a-z]+$/.test(str), isNumeric = str => /^[0-9]+$/.test(str);
    const deduceListType = start => {
        if (isNumeric(start)) return 2;
        else if (isUppercase(start)) return 0;
        else if (isLowercase(start)) return 1;
        else if (isEmpty$1(start)) return 3;
        return 4;
    };
    const parseStartValue = start => {
        switch (deduceListType(start)) {
            case 2: return Optional.some({listStyleType: Optional.none(), start});
            case 0: return Optional.some({listStyleType: Optional.some('upper-alpha'), start: parseAlphabeticBase26(start).toString()});
            case 1: return Optional.some({listStyleType: Optional.some('lower-alpha'), start: parseAlphabeticBase26(start).toString()});
            case 3: return Optional.some({listStyleType: Optional.none(), start: ''});
            case 4: return Optional.none();
        }
    };
    const parseDetail = detail => {
        if (is$2(detail.listStyleType, 'upper-alpha')) return composeAlphabeticBase26(parseInt(detail.start, 10));
        else if (is$2(detail.listStyleType, 'lower-alpha')) return composeAlphabeticBase26(parseInt(detail.start, 10)).toLowerCase();
        return detail.start;
    };
    const open = editor => {
        const currentList = getParentList(editor);
        if (!isOlNode(currentList) || isWithinNonEditableList(editor, currentList)) return;
        editor.windowManager.open({
            title: 'List Properties',
            body: {type: 'panel', items: [{type: 'input', name: 'start', label: 'Start list at number', inputMode: 'numeric'}]},
            initialData: {
                start: parseDetail({
                    start: editor.dom.getAttrib(currentList, 'start', '1'),
                    listStyleType: Optional.from(editor.dom.getStyle(currentList, 'list-style-type'))
                })
            },
            buttons: [
                {type: 'cancel', name: 'cancel', text: 'Cancel'},
                {type: 'submit', name: 'save', text: 'Save', primary: true}
            ],
            onSubmit: api => {
                const data = api.getData();
                parseStartValue(data.start).each(detail => {
                    editor.execCommand('mceListUpdate', false, {
                        attrs: {start: detail.start === '1' ? '' : detail.start},
                        styles: {'list-style-type': detail.listStyleType.getOr('')}
                    });
                });
                api.close();
            }
        });
    };
    const queryListCommandState = (editor, listName) => () => { return isNonNullable(getParentList(editor)) && getParentList(editor).nodeName === listName; };
    const registerDialog = editor => {
        editor.addCommand('mceListProps', () => { open(editor); });
    };
    const register$2 = editor => {
        editor.on('BeforeExecCommand', e => {
            const cmd = e.command.toLowerCase();
            if (cmd === 'indent') indentListSelection(editor);
            else if (cmd === 'outdent') outdentListSelection(editor);
        });
        editor.addCommand('InsertUnorderedList', (ui, detail) => { toggleList(editor, 'UL', detail); });
        editor.addCommand('InsertOrderedList', (ui, detail) => { toggleList(editor, 'OL', detail); });
        editor.addCommand('InsertDefinitionList', (ui, detail) => { toggleList(editor, 'DL', detail); });
        editor.addCommand('RemoveList', () => { flattenListSelection(editor); });
        registerDialog(editor);
        editor.addCommand('mceListUpdate', (ui, detail) => {
            if (isObject(detail)) updateList(editor, detail);
        });
        editor.addQueryStateHandler('InsertUnorderedList', queryListCommandState(editor, 'UL'));
        editor.addQueryStateHandler('InsertOrderedList', queryListCommandState(editor, 'OL'));
        editor.addQueryStateHandler('InsertDefinitionList', queryListCommandState(editor, 'DL'));
    };
    let global = tinymce.util.Tools.resolve('tinymce.html.Node');
    const isTextNode = node => node.type === 3, isEmpty = nodeBuffer => nodeBuffer.length === 0;
    const wrapInvalidChildren = list => {
        const insertListItem = (buffer, refNode) => {
            const li = global.create('li');
            each$1(buffer, node => li.append(node));
            if (refNode) list.insert(li, refNode, true);
            else list.append(li);
        };
        const reducer = (buffer, node) => {
            if (isTextNode(node)) return [...buffer, node];
            else if (!isEmpty(buffer) && !isTextNode(node)) {
                insertListItem(buffer, node);
                return [];
            }
            return buffer;
        };
        const restBuffer = foldl(list.children(), reducer, []);
        if (!isEmpty(restBuffer)) insertListItem(restBuffer);
    };
    const setup$1 = editor => {
        editor.on('PreInit', () => {
            const {parser} = editor;
            parser.addNodeFilter('ul,ol', nodes => each$1(nodes, wrapInvalidChildren));
        });
    };
    const setupTabKey = editor => {
        editor.on('keydown', e => {
            if (e.keyCode !== global$4.TAB || global$4.metaKeyPressed(e)) return;
            editor.undoManager.transact(() => {
                if (e.shiftKey ? outdentListSelection(editor) : indentListSelection(editor)) e.preventDefault();
            });
        });
    };
    const setup = editor => {
        if (shouldIndentOnTab(editor)) setupTabKey(editor);
        setup$2(editor);
    };
    const setupToggleButtonHandler = (editor, listName) => api => {
        const toggleButtonHandler = e => {
            api.setActive(inList(e.parents, listName));
            api.setEnabled(!isWithinNonEditableList(editor, e.element));
        };
        return setNodeChangeHandler(editor, toggleButtonHandler);
    };
    const register$1 = editor => {
        const exec = command => () => editor.execCommand(command);
        if (!editor.hasPlugin('advlist')) {
            editor.ui.registry.addToggleButton('numlist', {
                icon: 'ordered-list',
                active: false,
                tooltip: 'Numbered list',
                onAction: exec('InsertOrderedList'),
                onSetup: setupToggleButtonHandler(editor, 'OL')
            });
            editor.ui.registry.addToggleButton('bullist', {
                icon: 'unordered-list',
                active: false,
                tooltip: 'Bullet list',
                onAction: exec('InsertUnorderedList'),
                onSetup: setupToggleButtonHandler(editor, 'UL')
            });
        }
    };
    const setupMenuButtonHandler = (editor, listName) => api => {
        const menuButtonHandler = e => api.setEnabled(inList(e.parents, listName) && !isWithinNonEditableList(editor, e.element));
        return setNodeChangeHandler(editor, menuButtonHandler);
    };
    const register = editor => {
        const listProperties = {
            text: 'List properties...',
            icon: 'ordered-list',
            onAction: () => editor.execCommand('mceListProps'),
            onSetup: setupMenuButtonHandler(editor, 'OL')
        };
        editor.ui.registry.addMenuItem('listprops', listProperties);
        editor.ui.registry.addContextMenu('lists', {update: node => { return isOlNode(getParentList(editor, node)) ? ['listprops'] : []; }});
    };

    let Plugin = () => {
        global$7.add('lists', editor => {
            register$3(editor);
            setup$1(editor);
            if (!editor.hasPlugin('rtc', true)) {
                setup(editor);
                register$2(editor);
            } else registerDialog(editor);
            register$1(editor);
            register(editor);
            return get(editor);
        });
    };
    Plugin();
})();