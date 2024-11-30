// stores/mapStore.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useMapStore = defineStore('map', () => {
  const apiKey = '0836119f538d650272fc667d96b1a3e0'
  const map = ref(null)
  const latitude = ref(37.5665)
  const longitude = ref(126.9780)
  const bankList = ref([])
  const searchKeyword = ref('')
  const infowindow = ref(null)
  const ps = ref(null)
  const bs = ref(null)

  // 지도 초기화
  const initializeMap = () => {
    const script = document.createElement('script')
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${apiKey}&autoload=false`
    
    const scriptForLib = document.createElement('script')
    scriptForLib.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${apiKey}&libraries=services,clusterer,drawing&autoload=false`
    
    script.onload = () => {
      kakao.maps.load(fetchLocation)
    }

    document.body.appendChild(script)
    document.body.appendChild(scriptForLib)
  }

  // 현재 위치 가져오기
  const fetchLocation = () => {
    const options = {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0,
    }

    const success = (pos) => {
      const crd = pos.coords
      latitude.value = crd.latitude
      longitude.value = crd.longitude
      createMap()
    }

    const error = (err) => {
      console.warn(`ERROR(${err.code}): ${err.message}`)
      // 위치 정보를 가져오지 못할 경우 서울시청 좌표로 설정
      latitude.value = 37.5665 // 서울시청 위도
      longitude.value = 126.9780 // 서울시청 경도
      createMap() // 서울시청 위치로 지도 생성
    }

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(success, error, options)
    } else {
      alert("이 브라우저에서는 Geolocation이 지원되지 않습니다.")
    }
  }

  // 지도 생성
  const createMap = () => {
    const container = document.getElementById('map')
    const options = {
      center: new kakao.maps.LatLng(latitude.value, longitude.value),
      level: 5
    }

    map.value = new kakao.maps.Map(container, options)

    // 컨트롤 추가
    const basicControl = new kakao.maps.MapTypeControl()
    const zoomControl = new kakao.maps.ZoomControl()
    map.value.addControl(basicControl, kakao.maps.ControlPosition.TOPRIGHT)
    map.value.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT)

    // 장소 검색 객체 생성
    bs.value = new kakao.maps.services.Places(map.value)

    // 초기 은행 검색
    searchNearbyBanks()
  }

  // 마커 표시
  const displayMarker = (place) => {
    infowindow.value = new kakao.maps.InfoWindow({ zIndex: 1 })
    const marker = new kakao.maps.Marker({
      map: map.value,
      position: new kakao.maps.LatLng(place.y, place.x)
    })

    kakao.maps.event.addListener(marker, 'click', () => {
      infowindow.value.setContent(
        `<div style="padding:5px;font-size:12px;">${place.place_name}</div>`
      )
      infowindow.value.open(map.value, marker)
    })
  }


  // 키워드로 은행 검색
const searchByKeyword = () => {
  if (!searchKeyword.value) return

  ps.value = new kakao.maps.services.Places()
  bankList.value = [] // 검색 결과 초기화

  const placeSearchCB = (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      const bounds = new kakao.maps.LatLngBounds()
      let bankFound = false

      // 은행 결과만 필터링
      data.forEach(place => {
        // 카테고리가 은행이거나(BK9) 이름에 은행이 포함된 경우
        if (place.category_group_code === 'BK9' || 
            place.place_name.includes('은행')) {
          bankList.value.push(place)
          displayMarker(place)
          bounds.extend(new kakao.maps.LatLng(place.y, place.x))
          bankFound = true
        }
      })

      if (bankFound) {
        map.value.setBounds(bounds)
      } else {
        // 은행을 찾지 못한 경우 키워드에 '은행'을 추가하여 재검색
        ps.value.keywordSearch(searchKeyword.value + ' 은행', placeSearchCB)
      }
    } else {
      alert('검색 결과가 없습니다. 정확한 장소를 입력해주세요.')
    }
  }

  // 키워드 검색 실행
  ps.value.keywordSearch(searchKeyword.value, placeSearchCB, {
    category_group_code: 'BK9'  // 은행 카테고리로 제한
  })
}

  
  // 특정 위치 주변의 은행/ATM 검색
  const searchNearbyBanks = (latLng, radius = 5000) => { // 기본 반경을 5km로 설정
    const placeSearchCB = (data, status) => {
      if (status === kakao.maps.services.Status.OK) {
        const bounds = new kakao.maps.LatLngBounds()
        let bankFound = false
  
        data.forEach((place) => {
          if (place.category_group_code === 'BK9') {
            bankList.value.push(place)
            displayMarker(place)
            bounds.extend(new kakao.maps.LatLng(place.y, place.x))
            bankFound = true
          }
        })
  
        if (!bankFound) {
          alert('검색된 장소 주변에 은행 또는 ATM이 없습니다.')
        }
      } else {
        alert('은행 또는 ATM 검색에 실패했습니다. 다시 시도해주세요.')
      }
    }
  
    bs.value.categorySearch('BK9', placeSearchCB, {
      location: latLng,
      radius: radius, // 반경을 파라미터로 받아서 설정
      // size: 15 // 한번에 가져올 결과 수 증가
    })
  }


  return {
    map,
    latitude,
    longitude,
    bankList,
    searchKeyword,
    initializeMap,
    searchByKeyword,
  }
})