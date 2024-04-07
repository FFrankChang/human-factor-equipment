using System;
using System.IO;
using System.Net.Sockets;
using System.Net;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Threading;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;



namespace ConsoleSerialDllDemo
{
    class AxisBridge
    {
        public enum SerialStatus {
            CLOSED,
            OPENED,
            CONNECTED,
            TO_SAMPLE,
            SAMPLING,
            TO_STOP,
            STOPPED
        }

        public unsafe delegate void delegateRecevier(int code, int row, int col, int* pData);

        //AxisInterpreter
        [DllImport("AxisBridge.dll", CharSet = CharSet.Ansi, CallingConvention = CallingConvention.Cdecl)]
        public static extern bool openSerial(string port);

        [DllImport("AxisBridge.dll", CharSet = CharSet.Ansi, CallingConvention = CallingConvention.Cdecl)]
        public static extern bool closeSerial();
        [DllImport("AxisBridge.dll", CharSet = CharSet.Ansi, CallingConvention = CallingConvention.Cdecl)]
        public static extern void startSampling();

        [DllImport("AxisBridge.dll", CharSet = CharSet.Ansi, CallingConvention = CallingConvention.Cdecl)]
        public static extern void stopSampling();

        [DllImport("AxisBridge.dll", CharSet = CharSet.Ansi, CallingConvention = CallingConvention.Cdecl)]
        public static extern uint getCode();

        [DllImport("AxisBridge.dll", CharSet = CharSet.Ansi, CallingConvention = CallingConvention.Cdecl)]
        public static extern SerialStatus getStatus();

        [DllImport("AxisBridge.dll", CharSet = CharSet.Ansi, CallingConvention = CallingConvention.Cdecl)]
        public unsafe static extern void setReceiver(delegateRecevier receiver);

        [DllImport("AxisBridge.dll", CharSet = CharSet.Ansi, CallingConvention = CallingConvention.Cdecl)]
        public static extern double getSenselArea();
    }
    class Program
    {
        static string configFile = "config.json";
        static string comPort = null;
        static string address = null;
        static int port = 0;
        static string filePath = null;
        static string csvFilePath = null;
        static StreamWriter sWriter  = null;

        static UdpClient udpClient = null;
        static IPEndPoint serverEndPoint = null;

        public unsafe static void onReceiveData(int code, int row, int col, int* pData)
        {
            DateTime time = DateTime.Now;
            long timestamp = DateTimeOffset.Now.ToUnixTimeMilliseconds();
            Console.WriteLine("code = {0}, row = {1}, col = {2}, time = {3}", code, row, col,time);
            string title = $"code = {code}, row = {row}, col = {col},{time.ToString("yyyy-MM-dd HH:mm:ss.fff")},{timestamp}";
            sWriter.WriteLine(title);
            int index = 0;
            for (int i = 0; i < col; i++)
            {
                string line = "";
                for (int j = 0; j < row; j++)
                {
                    line += " " + pData[index++].ToString();
                }
                sWriter.WriteLine(line);
                Console.WriteLine($"{line}");
            }
            sWriter.Flush(); // 确保数据实时写入文件
        }

        public unsafe static void sendUdp(string dataToSend) 
        {
            byte[] dataBytes = System.Text.Encoding.UTF8.GetBytes(dataToSend);
            // 发送数据
            udpClient.Send(dataBytes, dataBytes.Length, serverEndPoint);
            Console.WriteLine($"udp data: {dataBytes},{System.Text.Encoding.UTF8.GetString(dataBytes)}");

        }
        static unsafe void Main(string[] args)
        {
            string json = File.ReadAllText(configFile);
            JObject config = JObject.Parse(json);
            comPort = config["com"].ToString();
            address = config["address"].ToString();
            port = int.Parse(config["port"].ToString());
            filePath = config["filePath"].ToString();
            string createDate = System.DateTime.Now.ToString("D");
            string time = System.DateTime.Now.ToString("t").Replace(":","_");

            // 创建UDP客户端
            IPAddress serverIp = IPAddress.Parse(address);
            serverEndPoint = new IPEndPoint(serverIp, port);
            udpClient = new UdpClient();
            
            

            if (!Directory.Exists(filePath))
            {
                DirectoryInfo directoryInfo = new DirectoryInfo(filePath);
                directoryInfo.Create();
            }

            csvFilePath = Path.Combine(filePath, "csv_data"+ createDate  + time + "t.csv");

            try {
                StreamWriter writer = new StreamWriter(csvFilePath);
                sWriter = writer;
            } catch (Exception e)
            {
                Console.WriteLine($"Writing data exception: {e}");
            }

            AxisBridge.setReceiver(onReceiveData);
            bool opened = AxisBridge.openSerial(comPort);
            if (!opened)
            {
                Console.WriteLine("打开串口失败，请检查串口连接情况: status = {0}", AxisBridge.getStatus());
                return;
            }
            Console.WriteLine("code = {0}, status = {1}, sensel_area = {2}", AxisBridge.getCode(), AxisBridge.getStatus(), AxisBridge.getSenselArea());
            for (int i = 0; i < 2; i++)
            {
                AxisBridge.closeSerial();
                Console.WriteLine("code = {0}, status = {1}, sensel_area = {2}", AxisBridge.getCode(), AxisBridge.getStatus(), AxisBridge.getSenselArea());

                AxisBridge.openSerial(comPort);
                Console.WriteLine("code = {0}, status = {1}, sensel_area = {2}", AxisBridge.getCode(), AxisBridge.getStatus(), AxisBridge.getSenselArea());

                //打开成功后状态如果还没有变成CONNECTED，startSampling会失败
                while (AxisBridge.getStatus() < AxisBridge.SerialStatus.CONNECTED)
                {
                    Console.WriteLine("wait until connected: status = {0}", AxisBridge.getStatus());
                    Thread.Sleep(200);
                }
                AxisBridge.startSampling();
                Console.WriteLine("code = {0}, status = {1}, sensel_area = {2}", AxisBridge.getCode(), AxisBridge.getStatus(), AxisBridge.getSenselArea());
                
                Thread.Sleep(20000);
                Console.WriteLine("code = {0}, status = {1}, sensel_area = {2}", AxisBridge.getCode(), AxisBridge.getStatus(), AxisBridge.getSenselArea());

                AxisBridge.stopSampling();
                Console.WriteLine("code = {0}, status = {1}, sensel_area = {2}", AxisBridge.getCode(), AxisBridge.getStatus(), AxisBridge.getSenselArea());

                Thread.Sleep(2000);
                Console.WriteLine("code = {0}, status = {1}, sensel_area = {2}", AxisBridge.getCode(), AxisBridge.getStatus(), AxisBridge.getSenselArea());
                sWriter.Dispose();
            }

            bool closed = AxisBridge.closeSerial();

            Console.WriteLine("code = {0}, status = {1}, sensel_area = {2}", AxisBridge.getCode(), AxisBridge.getStatus(), AxisBridge.getSenselArea());

            Console.WriteLine("opened = {0}, closed = {1}, thread = {2}", opened, closed, Thread.CurrentThread.ManagedThreadId);
        }
    }
}
