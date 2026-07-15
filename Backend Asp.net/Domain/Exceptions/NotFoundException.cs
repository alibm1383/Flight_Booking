using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace Domain.Exceptions
{
    public class NotFoundException : Exception
    {
        public HttpStatusCode StatusCode => HttpStatusCode.NotFound;
        public NotFoundException(string message):base(message)
        { 

        }
    }
}
