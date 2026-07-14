using Application.Services.Interfaces;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;
using System.Text;

namespace Application.Services.Implementations;

public class SmsSender : ISmsSender
{
    private readonly IConfiguration _configuration;
    public SmsSender(IConfiguration configuration)
    {
        _configuration = configuration;
    }
    public async Task SendSmsAsync(string to, string body)
    {
        try
        {
            using HttpClient httpClient = new HttpClient();
            httpClient.DefaultRequestHeaders.Add("x-api-key", _configuration["SmsSettings:x-api-key"]);

            var data = new
            {
                lineNumber = _configuration["SmsSettings:LineNumber"],
                messageText = body,
                mobiles = new[] { to },
                sendDateTime = (string?)null
            };

            var json = JsonConvert.SerializeObject(data);
            HttpContent content = new StringContent(json, Encoding.UTF8, "application/json");
            var response = await httpClient.PostAsync("https://api.sms.ir/v1/send/bulk", content);
            var result = await response.Content.ReadAsStringAsync();
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex);
        }
    }
}
