using Application.Services.Interfaces;
using AutoMapper;
using Domain.DTOs;
using Domain.Entities;
using Domain.Exceptions;
using Domain.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Services.Implementations
{
    public class BookingService : IBookingService
    {
        private readonly IBookingRepository _bookingRepository;
        private readonly IFlightRepository _flightRepository;
        private readonly IMapper _mapper;
        private readonly ISmsSender _smsSender;
        public BookingService(IBookingRepository bookingRepository
            , IFlightRepository flightRepository , IMapper mapper,ISmsSender smsSender)
        {
            _bookingRepository = bookingRepository;
            _flightRepository = flightRepository;
            _mapper = mapper;
            _smsSender = smsSender;
        }

        public async Task AddBookingAsync(CreateBookingDto createBookingDto)
        {
            var flight = await _flightRepository.GetFlightByIdAsync(createBookingDto.FlightId);
            if (flight == null)
            {
                throw new NotFoundException("Flight not found.");
            }
            if(flight.AvailableSeats < createBookingDto.Passengers.Count)
            {
                throw new BusinessException("Not enough seats.");
            }
            var booking = _mapper.Map<Booking>(createBookingDto);
            booking.BookingDate = DateTime.UtcNow;
            booking.PnrCode = PnrGenerator.Generate();
            flight.AvailableSeats -= createBookingDto.Passengers.Count;
            booking.TotalAmount = flight.Price * createBookingDto.Passengers.Count;
            booking.BookingDate = DateTime.UtcNow;
            await _bookingRepository.AddBookingAsync(booking);
            //TODO unit of work
            await _bookingRepository.SaveChangesAsync();
            string message = $"پرواز شما با موفقیت رزرو شد.\n شماره رزرو : {booking.PnrCode}";
            await _smsSender.SendSmsAsync("09372792737", message);
        }

        public async Task<List<BookingDto>> GetBookingsByUserId(int userId)
        {
            return await _bookingRepository.GetBookingsByUserId(userId);
        }

        public async Task<List<PassengerDto>> GetPassengersByBookingId(int bookingId)
        {
            var passengers = await _bookingRepository.GetPassengersByBookingId(bookingId);
            return _mapper.Map<List<PassengerDto>>(passengers);
        }
    }
}
