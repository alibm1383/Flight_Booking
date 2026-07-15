using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace Domain.Exceptions
{
    public class BusinessException : Exception
    {
        public HttpStatusCode StatusCode => HttpStatusCode.BadRequest;
        public BusinessException(string message):base(message)
        {
            
        }
    }
}
