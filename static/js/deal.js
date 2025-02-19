(() => {
    'use strict'
    const price = document.getElementById('id_price'),
        com_agent = document.getElementById('id_agent'),
        com_agent_percent = document.getElementById('com_agent_percent'),
        com_manager = document.getElementById('id_manager'),
        com_manager_percent = document.getElementById('com_manager_percent');
    if (parseFloat(price.value) > 0) {
        if (parseFloat(com_agent.value) > 0) {
            com_agent_percent.value = (parseFloat(com_agent.value) / parseFloat(price.value) * 100).toFixed(2);
        }
        if (parseFloat(com_manager.value) > 0) {
            com_manager_percent.value = (parseFloat(com_manager.value) / parseFloat(price.value) * 100).toFixed(2);
        }
    }
    price.addEventListener('input', (evt) => {
        let result = (evt.target.value * com_agent_percent.value / 100).toFixed(2);
        if (Number.isNaN(result)) com_agent.value = 0;
        else com_agent.value = result;
        result = (evt.target.value * com_manager_percent.value / 100).toFixed(2);
        if (Number.isNaN(result)) com_manager.value = 0;
        else com_manager.value = result;
    });
    com_agent.addEventListener('input', (evt) => {
        let result = (parseFloat(evt.target.value) / parseFloat(price.value) * 100).toFixed(2);
        if (Number.isNaN(result)) com_agent_percent.value = 0;
        else com_agent_percent.value = result;
    });
    com_agent_percent.addEventListener('input', (evt) => {
        let result = (parseFloat(evt.target.value) * parseFloat(price.value) / 100).toFixed(2);
        if (Number.isNaN(result)) com_agent.value = 0;
        else com_agent.value = result;
    });
    com_manager.addEventListener('input', (evt) => {
        let result = (parseFloat(evt.target.value) / parseFloat(com_agent.value) * 100).toFixed(2);
        if (Number.isNaN(result)) com_manager_percent.value = 0;
        else com_manager_percent.value = result;
    });
    com_manager_percent.addEventListener('input', (evt) => {
        let result = (parseFloat(evt.target.value) * parseFloat(com_agent.value) / 100).toFixed(2);
        if (Number.isNaN(result)) com_manager.value = 0;
        else com_manager.value = result;
    });
})();