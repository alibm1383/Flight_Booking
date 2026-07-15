using Application.Services.Interfaces;
using Domain.DTOs;
using Microsoft.AspNetCore.Authorization;
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

        [Authorize]
        [HttpGet()]
        public async Task<IActionResult> GetMyBookings()
        {
            var userId = int.Parse(User.FindFirst("user_id")!.Value);
            var bookings = await _bookingService.GetBookingsByUserId(userId);
            return Ok(bookings);
        }

        [Authorize]
        [HttpGet("{bookingId}/passengers")]
        public async Task<IActionResult> GetPassengersByBookingId(int bookingId)
        {
            var userId = int.Parse(User.FindFirst("user_id")!.Value);
            var passengers = await _bookingService.GetPassengersByBookingId(bookingId,userId);
            return Ok(passengers);
        }

        [Authorize]
        [HttpPost]
        public async Task<IActionResult> Post([FromBody] CreateBookingDto createBookingDto)
        {
            var userId = int.Parse(User.FindFirst("user_id")!.Value);
            await _bookingService.AddBookingAsync(createBookingDto ,userId);
            return Created();
        }
    }
}
