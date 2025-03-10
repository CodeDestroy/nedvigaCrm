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
    const fireVisualBlocks = (editor, state) => { editor.dispatch('VisualBlocks', {state}); };
    const toggleVisualBlocks = (editor, pluginUrl, enabledState) => {
        editor.dom.toggleClass(editor.getBody(), 'mce-visualblocks');
        enabledState.set(!enabledState.get());
        fireVisualBlocks(editor, enabledState.get());
    };
    const register$2 = (editor, pluginUrl, enabledState) => {
        editor.addCommand('mceVisualBlocks', () => { toggleVisualBlocks(editor, pluginUrl, enabledState); });
    };
    const option = name => editor => editor.options.get(name);
    const register$1 = editor => { editor.options.register('visualblocks_default_state', {processor: 'boolean', default: false}); };
    const isEnabledByDefault = option('visualblocks_default_state');
    const setup = (editor, pluginUrl, enabledState) => {
        editor.on('PreviewFormats AfterPreviewFormats', e => {
            if (enabledState.get()) editor.dom.toggleClass(editor.getBody(), 'mce-visualblocks', e.type === 'afterpreviewformats');
        });
        editor.on('init', () => {
            if (isEnabledByDefault(editor)) toggleVisualBlocks(editor, pluginUrl, enabledState);
        });
    };
    const toggleActiveState = (editor, enabledState) => api => {
        api.setActive(enabledState.get());
        const editorEventCallback = e => api.setActive(e.state);
        editor.on('VisualBlocks', editorEventCallback);
        return () => editor.off('VisualBlocks', editorEventCallback);
    };
    const register = (editor, enabledState) => {
        const onAction = () => editor.execCommand('mceVisualBlocks');
        editor.ui.registry.addToggleButton('visualblocks', {icon: 'visualblocks', tooltip: 'Show blocks', onAction, onSetup: toggleActiveState(editor, enabledState)});
        editor.ui.registry.addToggleMenuItem('visualblocks', {text: 'Show blocks', icon: 'visualblocks', onAction, onSetup: toggleActiveState(editor, enabledState)});
    };
    let Plugin = () => {
        global.add('visualblocks', (editor, pluginUrl) => {
            register$1(editor);
            const enabledState = Cell(false);
            register$2(editor, pluginUrl, enabledState);
            register(editor, enabledState);
            setup(editor, pluginUrl, enabledState);
        });
    };
    Plugin();
})();