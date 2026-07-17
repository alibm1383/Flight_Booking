using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace Domain.Exceptions
{
    public class ForbiddenException : Exception
    {
        public HttpStatusCode StatusCode => HttpStatusCode.Forbidden;
        public ForbiddenException(string message) : base(message)
        {
                    
        }
    }
}
