import QtQuick 2.0
import QtQuick.Window 2.0
import "material"

Window {
    id: root
    visible: true
    width: 720 * dp
    height: 560 * dp
    title: "Corpora"
    color: "#eee"

    Item {
        id: messageArea
        anchors {
            top: parent.top
            right: tabArea.left
            bottom: parent.bottom
            left: parent.left
        }

        Rectangle {
            id: background
            anchors.fill: parent
            color: "white"
            visible: false
        }

        PaperShadow {
            source: background
            depth: 2
            cached: true
            fast: true
        }

        Rectangle {
            id: footer
            anchors {
                left: parent.left
                right: parent.right
                bottom: parent.bottom
            }
            height: field.height
            color: "white"

            TextField {
                id: field
                anchors {
                    left: parent.left
                    right: sendButton.left
                    margins: 16 * dp
                }
                hint: "留言⋯⋯"

                Keys.onReturnPressed: {
                    if (length > 0) sendButton.clicked()
                }
            }

            IconButton {
                id: sendButton
                anchors {
                    verticalCenter: parent.verticalCenter
                    right: parent.right
                    margins: 16 * dp
                }
                iconSource: "qrc:/assets/icon_send"

                enabled: (field.length > 0)
                onClicked: {
                    client.sendEvent({"action": "message", "content": field.text})
                    field.text = ""
                }
            }
        }
    }

    Item {
        id: tabArea
        anchors {
            top: parent.top
            right: parent.right
            bottom: parent.bottom
        }
        width: Math.min(parent.width * 0.33, 320 * dp)
    }

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
