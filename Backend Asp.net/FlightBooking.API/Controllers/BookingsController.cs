using Application.Services.Interfaces;
using Domain.DTOs;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System.Security.Cryptography.X509Certificates;

namespace FlightBooking.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class BookingsController : ControllerBase
    {
        private readonly IBookingService _bookingService;
        public BookingsController(IBookingService bookingService)
        {
            _bookingService = bookingService;
        }


        [HttpGet("{userId}")]
        public async Task<IActionResult> GetBookingsByUserId(int userId)
        {
            var bookings = await _bookingService.GetBookingsByUserId(userId);
            return Ok(bookings);
        }

        [HttpGet("{bookingId}/passengers")]
        public async Task<IActionResult> GetPassengersByBookingId(int bookingId)
        {
            var passengers = await _bookingService.GetPassengersByBookingId(bookingId);
            return Ok(passengers);
        }


        [HttpPost]
        public async Task<IActionResult> Post([FromBody] CreateBookingDto createBookingDto)
        {
            await _bookingService.AddBookingAsync(createBookingDto);
            return Created();
        }
    }
}
