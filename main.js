const { app, BrowserWindow } = require('electron')
app.commandLine.appendSwitch('ignore-certificate-errors')
const path = require('path')

const createWindows = () => {
    const window = new BrowserWindow({
        width:700,
        height: 400,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            preload: path.join(__dirname, 'preload.js')
        }
    })
    // const login = new BrowserWindow({
    //     parent: window,
    //     width:400,
    //     height:300,
    //     frame:false
    // })
    window.loadFile('index.html')
    // login.loadFile('login.html')
}

app.whenReady().then(() => {
    createWindows()

// Mac open new window if none open
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
      })
})

//Linux / Win kill app on window close
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit()
  })

