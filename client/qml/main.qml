import QtQuick 2.0
import QtQuick.Window 2.0

Window {
    id: root
    visible: true
    width: 720 * dp
    height: 560 * dp
    title: "Corpora"
    color: "white"

    Connections {
        target: client

        onConnected: {
            console.log("Connected")
        }

        onDisconnected: {
            console.log("Disconnected")
        }

        onError: {
            console.log("Socket error " + error)
            if (error == 0) {
                // Connection refused
            }
            else {
                // Generic error
            }
        }
    }

    Component.onCompleted: {
        client.connectToServer();
    }
}
