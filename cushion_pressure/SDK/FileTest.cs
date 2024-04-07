using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace AxisBridgeConsoleDemo
{
    class FileTest
    {
        static unsafe void Main(string[] args)
        {
            try
            {
                // 读取文本文件
                using (StreamReader sr = new StreamReader("config.txt"))
                {
                    string line;
                    // ReadLine()一行一行的循环读取
                    //当然可以直接ReadToEnd()读到最后
                    while ((line = sr.ReadLine()) != null)
                    {
                        Console.WriteLine(line);
                    }

                    Thread.Sleep(10000);
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
        }
    }


}
