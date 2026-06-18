using Application.Services.Interfaces;
using Domain.DTOs;
using Microsoft.AspNetCore.Mvc;

namespace FlightBooking.API.Controllers
{
    
    [Route("api/[controller]")]
    [ApiController]
    public class AirportsController : Controller
    {
        private readonly IAirportService _airportService;

        #region constructor
        public AirportsController(IAirportService airportService)
        {
            _airportService = airportService;
        }
        #endregion


        [HttpGet]
        public async Task<ActionResult<IEnumerable<AirportDto>>> Get()
        {
            var airports = await _airportService.GetAllAirportsAsync();
            return Ok(airports);
        }


        [HttpGet("{airportId}")]
        public async Task<IActionResult> Get(int airportId)
        {
            var airport = await _airportService.GetAirportByIdAsync(airportId);
            if (airport == null)
            {
                return NotFound();
            }
            return Ok(airport);
        }


        [HttpPost]
        public async Task<IActionResult> Post([FromForm] CreateAirportDto createAirportDto)
        {
            //TODO  Check airport doesnt exist
            await _airportService.AddAirportAsync(createAirportDto);
            return Created();
        }

    }
}
