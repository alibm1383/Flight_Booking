using Application.Services.Interfaces;
using Domain.DTOs;
using Domain.Entities;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

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


        [HttpGet]
        public  async Task<ActionResult<IEnumerable<CityDto>>> Get()
        {
            var cities =  await _cityService.GetAllCitiesAsync();
            return Ok(cities);
        }

        
        [HttpGet("{cityId}")]
        public async Task<IActionResult> Get(int cityId)
        {
            var city = await _cityService.GetCityByCityIdAsync(cityId);
            if (city == null)
            {
                return NotFound();
            }
            return Ok(city);
        }

        
        [HttpPost]
        public async Task<IActionResult> Post([FromForm] CreateCityDto createCityDto)
        {
           await _cityService.AddCityAsync(createCityDto);
           return Created();
        }

    }
}
