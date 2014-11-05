#include "client.h"

CorporaClient::CorporaClient(QObject *parent) :
    QObject(parent)
{
    this->m_host = "127.0.0.1";
    this->m_port = 1126;
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

}

void CorporaClient::sendEvent(QObject obj) {

}

void CorporaClient::disconnectFromServer() {

}
