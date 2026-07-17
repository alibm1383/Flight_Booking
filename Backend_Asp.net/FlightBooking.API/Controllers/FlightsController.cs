using Application.Services.Interfaces;
using Domain.DTOs;
using Domain.Exceptions;
using Microsoft.AspNetCore.Authorization;
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

        [Authorize(Roles = "2")]
        [HttpGet("airline")]
        public async Task<IActionResult> GetFlightsByAirlineId()
        {
            var airlineId = int.Parse(User.FindFirst("user_id")!.Value);
            var flights = await _flightService.GetFlightsByAirlineIdAsync(airlineId);
            return Ok(flights);
        }

        [Authorize(Roles = "2")]
        [HttpGet("{flightId}/passengers")]
        public async Task<IActionResult> GetPassengers(int flightId)
        {
            var airlineId = int.Parse(User.FindFirst("user_id")!.Value);
            var passengers = await _flightService.GetPassengersByFlightIdAsync(flightId,airlineId);
            return Ok(passengers);
        }

        [Authorize(Roles = "2")]
        [HttpPost]
        public async Task<IActionResult> Post([FromBody] CreateFlightDto createFlightDto)
        {
            var airlineId = int.Parse(User.FindFirst("user_id")!.Value);
            await _flightService.AddFlightAsync(createFlightDto,airlineId);
            return Created();
        }
    }
}
