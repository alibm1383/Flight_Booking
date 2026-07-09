using Application.Services.Interfaces;
using AutoMapper;
using Domain.DTOs;
using Domain.Entities;
using Domain.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Services.Implementations
{
    public class AirportService : IAirportService
    {
        private readonly IAirportRepository _airportReposiroty;
        private readonly IMapper _mapper;
        private readonly IFileService _fileService;

        #region Constructor
        public AirportService(IAirportRepository airportReposiroty, IMapper mapper, IFileService fileService)
        {
            _airportReposiroty = airportReposiroty;
            _mapper = mapper;
            _fileService = fileService;
        }
        #endregion

        public async Task AddAirportAsync(CreateAirportDto createAirportDto)
        {
            string? imagePath = null;
            if (createAirportDto.Image != null)
            {
                imagePath = await _fileService.UploadImageAsync(createAirportDto.Image , "airports");
            }

            var airport = new Airport()
            {
                CityId = createAirportDto.CityId,
                IataCode = createAirportDto.IataCode,
                Name = createAirportDto.Name,
                ImageUrl = imagePath
            };

            await _airportReposiroty.AddAirportAsync(airport);
            await _airportReposiroty.SaveChangesAsync();
        }

        public async Task<AirportDto?> GetAirportByIdAsync(int airportId)
        {
            var airport = await _airportReposiroty.GetAirportByIdAsync(airportId);
            return _mapper.Map<AirportDto>(airport);
        }

        public async Task<IEnumerable<AirportDto>> GetAllAirportsAsync()
        {
            var airports = await _airportReposiroty.GetAllAirportsAsync();
            return _mapper.Map<IEnumerable<AirportDto>>(airports);
        }
    }
}
