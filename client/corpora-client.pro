TEMPLATE = app

TARGET = Corpora

QT += qml quick network svg

HEADERS += \
    src/client.h

SOURCES += src/main.cpp \
    src/client.cpp

RESOURCES += qml/assets.qrc

OTHER_FILES += qml/*.qml

mac {
    QMAKE_MAC_SDK = macosx10.9
}
