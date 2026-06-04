using Application.Services.Interfaces;
using Domain.Entities;
using Microsoft.AspNetCore.Mvc;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace FlightBooking.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CitiesController : ControllerBase
    {
        private readonly ICityService _cityService;

        #region constructor
        public CitiesController(ICityService cityService)
        {
            _cityService = cityService;
        }
        #endregion



        // GET: api/<CitiesController>
        [HttpGet]
        public  async Task<IEnumerable<City>> Get()
        {
            return await _cityService.GetAllCitiesAsync();
        }

        // GET api/<CitiesController>/5
        [HttpGet("{id}")]
        public async Task<City?> Get(int cityId)
        {
            return await _cityService.GetCityByCityIdAsync(cityId);
        }

        // POST api/<CitiesController>
        [HttpPost]
        public void Post([FromBody]string value)
        {
        }

        // PUT api/<CitiesController>/5
        [HttpPut("{id}")]
        public void Put(int id, [FromBody]string value)
        {
        }

        // DELETE api/<CitiesController>/5
        [HttpDelete("{id}")]
        public void Delete(int id)
        {
        }
    }
}
