using System.Net;

namespace FlightBooking.API
{
    public class ExceptionMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<ExceptionMiddleware> _logger;

        public ExceptionMiddleware(RequestDelegate next, ILogger<ExceptionMiddleware> logger)
        {
            _next = next;
            _logger = logger;
        }

        public async Task Invoke(HttpContext context)
        {
            try
            {
                await _next(context);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex,
                "Unhandled exception. Method: {Method}, Path: {Path}",
                context.Request.Method,
                context.Request.Path);

                context.Response.ContentType = "application/json";

                var statusCode = HttpStatusCode.InternalServerError;

                var property = ex.GetType().GetProperty("StatusCode");
                if (property?.GetValue(ex) is HttpStatusCode code)
                {
                    statusCode = code;
                }

                context.Response.StatusCode = (int)statusCode;

                await context.Response.WriteAsJsonAsync(new
                {
                    message = ex.Message
                });
            }
        }
    }
}
