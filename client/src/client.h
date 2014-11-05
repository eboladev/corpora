#ifndef CLIENT_H
#define CLIENT_H

#include <QObject>
#include <QTcpSocket>

class CorporaClient : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString host READ host WRITE setHost)
    Q_PROPERTY(int port READ port WRITE setPort)

public:
    explicit CorporaClient(QObject *parent = 0);

    QString host();
    int port();

    void setHost(const QString &value);
    void setPort(const int &value);

    Q_INVOKABLE void connectToServer();
    Q_INVOKABLE void sendEvent(const QVariantMap &data);
    Q_INVOKABLE void disconnectFromServer();

signals:
    void connected();
    void serverEvent(const QVariantMap &data);
    void disconnected();
    void error(QAbstractSocket::SocketError);

private slots:
    void readFromServer();

private:
    QString m_host;
    int m_port;
    QTcpSocket* socket;

};

#endif // CLIENT_H
