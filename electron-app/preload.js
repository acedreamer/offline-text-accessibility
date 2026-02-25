const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  simplify: (payload) => ipcRenderer.invoke('simplify', payload)
})
