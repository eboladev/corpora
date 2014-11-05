#include "client.h"
#include <QJsonDocument>
#include <QJsonObject>

CorporaClient::CorporaClient(QObject *parent) :
    QObject(parent)
{
    this->m_host = "127.0.0.1";
    this->m_port = 1126;
    this->socket = new QTcpSocket(this);

    connect(socket, SIGNAL(connected()), this, SIGNAL(connected()));
    connect(socket, SIGNAL(disconnected()), this, SIGNAL(disconnected()));
    connect(socket, SIGNAL(error(QAbstractSocket::SocketError)), this, SIGNAL(error(QAbstractSocket::SocketError)));
    connect(socket, SIGNAL(readyRead()), this, SLOT(readFromServer()));
}

QString CorporaClient::host() {
    return this->m_host;
}

int CorporaClient::port() {
    return this->m_port;
}

void CorporaClient::setHost(const QString &value) {
    this->m_host = value;
}

void CorporaClient::setPort(const int &value) {
    this->m_port = value;
}

void CorporaClient::connectToServer() {
    socket->connectToHost(m_host, m_port);
}

void CorporaClient::readFromServer() {
    if (socket->canReadLine()) {
        QByteArray buffer;
        buffer = socket->readLine();

        if (buffer.length() > 0) {
            QJsonDocument doc = QJsonDocument::fromJson(buffer);

            if (doc.isObject())
                this->serverEvent(doc.object());
        }
    }
}

void CorporaClient::sendEvent(const QVariantMap &data) {
    QJsonDocument doc = QJsonDocument::fromVariant(data);
    QByteArray buffer = doc.toJson(QJsonDocument::Compact);
    buffer.append('\n');

    socket->write(buffer);
}

void CorporaClient::disconnectFromServer() {
    socket->disconnectFromHost();
}
