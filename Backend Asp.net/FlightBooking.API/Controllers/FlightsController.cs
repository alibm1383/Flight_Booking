using Application.Services.Interfaces;
using Domain.DTOs;
using Microsoft.AspNetCore.Mvc;

namespace FlightBooking.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FlightsController : ControllerBase
    {
        private readonly IFlightService _flightService;

        #region constructor
        public FlightsController(IFlightService flightService)
        {
            _flightService = flightService;
        }
        #endregion


        [HttpGet]
        public async Task<ActionResult<IEnumerable<FlightDto>>> Get()
        {
            var flights = await _flightService.GetAllFlightsAsync();
            return Ok(flights);
        }


        [HttpGet("{flightId}")]
        public async Task<IActionResult> Get(int flightId)
        {
            var flight = await _flightService.GetFlightByIdAsync(flightId);
            if (flight == null)
            {
                return NotFound();
            }
            return Ok(flight);
        }


        [HttpPost]
        public async Task<IActionResult> Post([FromBody] CreateFlightDto createFlightDto)
        {
            await _flightService.AddFlightAsync(createFlightDto);
            return Created();
        }

    }
}
