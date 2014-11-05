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

    property string currentChannel: "#general"

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

        ListView {
            id: messages
            anchors {
                top: parent.top
                right: parent.right
                bottom: footer.top
                left: parent.left
            }
            topMargin: 8 * dp
            bottomMargin: 8 * dp
            leftMargin: 8 * dp
            rightMargin: 8 * dp
            spacing: 8 * dp
            model: ListModel {
                ListElement { username: "system"; content: "請以 /login 登入" }
            }
            delegate: Component {
                Text {
                    id: __text
                    width: messages.width
                    wrapMode: Text.Wrap
                    font.family: UIConstants.sansFontFamily
                    font.pointSize: UIConstants.bodyFontSize
                    color: "#de000000"
                    text: model.content ?
                          "<font color='#00796b'><b>" + model.username + "</b>: </font>" + model.content :
                          ""
                }
            }
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
                    if (field.text.indexOf("/login ") == 0) {
                        field.text = field.text.substring(7)
                        client.sendEvent({"action": "login", "user": field.text})
                    }
                    else
                        client.sendEvent({"action": "message", "content": field.text, "channel": currentChannel})
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

        Column {
            anchors {
                fill: parent
                topMargin: 56 * dp
            }

            Repeater {
                id: channels
                delegate: Component {
                    MenuItem {
                        text: modelData
                        enabled: (currentChannel != modelData)
                        onClicked: currentChannel = modelData
                    }
                }
            }
        }

        Text {
            id: statusText
            anchors {
                top: parent.top
                left: parent.left
                margins: 16 * dp
            }
            font.family: UIConstants.sansFontFamily
            font.pointSize: UIConstants.bodyFontSize
            color: UIConstants.displayTextColor
            text: "連線中"
        }

        IconButton {
            id: menuButton
            anchors {
                top: parent.top
                right: parent.right
                margins: 16 * dp
            }
            iconSource: "qrc:/assets/icon_menu"
        }
    }

    Connections {
        target: client

        onConnected: {
            console.log("Connected")
            statusText.text = "已連線"
        }

        onDisconnected: {
            console.log("Disconnected")
            statusText.text = "已離線"
        }

        onServerEvent: {
            if (data.status == "message")
                messages.model.append({"username": data.username, "content": data.content})
            else if (data.status == "success") {
                if (data.reason == "logged_in") {
                    messages.model.append({"username": "system", "content": "登入成功！"})
                    client.sendEvent({"action": "join", "channel": "#general"})
                }
                else if (data.reason == "joined_channel") {
                    channels.model = [data.channel]
                    messages.model.append({"username": "system", "content": "已加入頻道 " + data.channel })
                }
            }
            else if (data.status == "error") {
                if (data.reason == "name_in_use") {
                    messages.model.append({"username": "system", "content": "名稱已被使用。"})
                }
            }
            console.log("Server replied with status " + data.status)
        }

        onError: {
            console.log("Socket error " + error)
            if (error == 0) {
                // Connection refused
                statusText.text = "無法連線"
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
