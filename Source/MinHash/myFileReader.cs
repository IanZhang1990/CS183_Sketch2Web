using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace MinHashProgram
{
    class myFileReader
    {
        private StreamReader sr = null;

        public myFileReader(string filename)
        {
            sr = new StreamReader(filename);
        }

        public List<double> GetArray()
        {
            List<double> set = new List<double>();

            // read txt file
            string line = null;
            int number = int.Parse(sr.ReadLine());
            while ((line = sr.ReadLine()) != null)
            {
                string[] nums = line.Split(' ');
                for (int i = 0; i < nums.Length; i++)
                {
                    set.Add( Double.Parse(nums[i]) );
                }
            }

            return set;
        }
    }
}
