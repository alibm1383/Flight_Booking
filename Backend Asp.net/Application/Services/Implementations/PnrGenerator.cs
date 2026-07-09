using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Services.Implementations
{
    public static class PnrGenerator
    {
        public static string Generate()
        {
            return Guid.NewGuid().ToString("N").Substring(0, 10).ToUpper();
        }
    }
}
