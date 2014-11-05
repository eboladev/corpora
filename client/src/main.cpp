#include <QtGui/QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QScreen>
#include "client.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    app.setApplicationName("Corpora");
    app.setOrganizationName("NTUOSC");
    app.setOrganizationDomain("ntuosc.org");

    QQmlApplicationEngine engine;
    CorporaClient client(&app);
    qreal dp = 1; //QGuiApplication::primaryScreen()->physicalDotsPerInch() / 160.0;
    engine.rootContext()->setContextProperty("dp", dp);
    engine.rootContext()->setContextProperty("client", &client);
    engine.load(QUrl("qrc:/main.qml"));

    return app.exec();
}
