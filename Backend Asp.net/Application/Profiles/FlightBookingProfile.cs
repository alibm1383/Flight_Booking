using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using AutoMapper;
using Domain.DTOs;
using Domain.Entities;

namespace Application.Profiles
{
    public class FlightBookingProfile : Profile
    {
        public FlightBookingProfile()
        {
            CreateMap<City, CityDto>().ReverseMap();
            CreateMap<Airport, AirportDto>().ReverseMap();
            CreateMap<Flight, FlightDto>().ReverseMap();
            CreateMap<Flight, CreateFlightDto>().ReverseMap();
            CreateMap<Passenger, PassengerDto>().ReverseMap();
            CreateMap<Passenger, CreatePassengerDto>().ReverseMap();
            CreateMap<Booking, BookingDto>().ReverseMap();
            CreateMap<Booking, CreateBookingDto>().ReverseMap();
        }
    }
}
