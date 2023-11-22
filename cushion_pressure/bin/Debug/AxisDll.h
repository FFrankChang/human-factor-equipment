
#ifndef AXISDLL_H
#define AXISDLL_H

#if defined _WIN32 || defined __CYGWIN__
#ifdef BUILDING_DLL
#ifdef __GNUC__
#define DLL_PUBLIC __attribute__ ((dllexport))
#else
#define DLL_PUBLIC __declspec(dllexport) // Note: actually gcc seems to also supports this syntax.
#endif
#else
#ifdef __GNUC__
#define DLL_PUBLIC __attribute__ ((dllimport))
#else
#define DLL_PUBLIC __declspec(dllimport) // Note: actually gcc seems to also supports this syntax.
#endif
#endif
#define DLL_LOCAL
#else
#if __GNUC__ >= 4
#define DLL_PUBLIC __attribute__ ((visibility ("default")))
#define DLL_LOCAL  __attribute__ ((visibility ("hidden")))
#else
#define DLL_PUBLIC
#define DLL_LOCAL
#endif
#endif

//C#的bool是4个字节，所以。。。。
using BOOL = int;
typedef enum {
    CLOSED,
    OPENED,
    CONNECTED,
    TO_SAMPLE,
    SAMPLING,
    TO_STOP,
    STOPPED
} SerialStatus;

typedef void (*funcReceiver)(int code, int row, int col, int* pData);

//使用接口方式调用，先通过getBridge()获取实例
class DLL_PUBLIC ISerialBridge {
public:
    virtual BOOL openSerial(char* port) = 0;
    virtual BOOL closeSerial() = 0;
    virtual void startSampling() = 0;
    virtual void stopSampling() = 0;
    void setReceiver(funcReceiver onReceive);
    virtual unsigned int getCode() = 0;
    virtual SerialStatus getStatus() = 0;
    virtual double getSenselArea() = 0;
};

extern "C" {
    //C#: CharSet = CharSet.Ansi, CallingConvention = CallingConvention.Cdecl
    DLL_PUBLIC ISerialBridge* getBridge(); //for c/cpp calling

    //注册回调，用于接收压力数据
    DLL_PUBLIC void setReceiver(funcReceiver onReceive);

    //打开串口，正常情况下，状态会依次变成OPENED、CONNECTED
    DLL_PUBLIC bool openSerial(char* port);

    //关闭串口，关闭后状态会变成CLOSED
    DLL_PUBLIC bool closeSerial();

    //开始采样，在打开串口以后调用，正常情况下状态会依次变成TO_SAMPLE, SAMPLING
    DLL_PUBLIC void startSampling();

    //停止采样，正常情况下状态会依次变成TO_STOP, STOPPED
    DLL_PUBLIC void stopSampling();

    //读取编号，在状态>=CONNECTED状态才能获取到有效值
    DLL_PUBLIC unsigned int getCode();

    //读取状态，可随时获取，初始状态为CLOSED
    DLL_PUBLIC SerialStatus getStatus();

    //读取传感单元的面积，单位平方厘米，在状态>=CONNECTED状态才能获取到有效值
    DLL_PUBLIC double getSenselArea();
}

#endif // AXISDLL_H
