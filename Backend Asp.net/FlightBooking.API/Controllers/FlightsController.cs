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
        public async Task<ActionResult<PagedResult<FlightDto>>> Search([FromQuery]SearchFlightDto searchFlightDto)
        {
            var flights = await _flightService.SearchAsync(searchFlightDto);
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

        [HttpGet("airline/{airlineId}")]
        public async Task<IActionResult> GetFlightsByAirlineId(int airlineId)
        {
            var flights = await _flightService.GetFlightsByAirlineIdAsync(airlineId);
            return Ok(flights);
        }

        [HttpGet("{flightId}/passengers")]
        public async Task<IActionResult> GetPassengers(int flightId)
        {
            var passengers = await _flightService.GetPassengersByFlightIdAsync(flightId);
            return Ok(passengers);
        }

        [HttpPost]
        public async Task<IActionResult> Post([FromBody] CreateFlightDto createFlightDto)
        {
            await _flightService.AddFlightAsync(createFlightDto);
            return Created();
        }

    }
}
