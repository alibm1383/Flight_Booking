using Application.Services.Interfaces;
using AutoMapper;
using Domain.DTOs;
using Domain.Entities;
using Domain.Interfaces;
using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Services.Implementations
{
    public class CityService : ICityService
    {
        private readonly ICityRepository _cityRepository;
        private readonly IMapper _mapper;
        private readonly IFileService _fileService;

        #region Constructor
        public CityService(ICityRepository cityRepository, IMapper mapper, IFileService fileService)
        {
            _cityRepository = cityRepository;
            _mapper = mapper;
            _fileService = fileService;
        }
        #endregion

        public async Task AddCityAsync(CreateCityDto createCityDto)
        {
            string? imagePath = null;
            if (createCityDto.Image != null)
            {
                imagePath = await _fileService.UploadImageAsync(createCityDto.Image , "cities");
            }

            var city = new City()
            {
                Name = createCityDto.Name,
                ImageUrl = imagePath
            };

            await _cityRepository.AddCityAsync(city);
            await _cityRepository.SaveChangesAsync();
        }

        public async Task<IEnumerable<CityDto>> GetAllCitiesAsync()
        {
            var cities = await _cityRepository.GetAllCitiesAsync();
            return _mapper.Map<IEnumerable<CityDto>>(cities);
        }

        public async Task<CityDto?> GetCityByCityIdAsync(int cityId)
        {
            var city = await _cityRepository.GetCityByCityIdAsync(cityId);
            return _mapper.Map<CityDto?>(city);
        }
       
    }
}
