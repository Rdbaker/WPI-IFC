showTotalAttendance = (data) ->
  document.getElementById('attendance-total').innerText = data.total_guests

showHostGuestAttendance = (data) ->
  hostData = {}
  hostData[d[0]] = {'attended': d[1]} for d in data.host_attendance_normalized
  hostData[d[0]]['listed'] = d[1] for d in data.host_attendance_raw

  orderedHosts = Object.keys(hostData).sort (a, b) ->
    hostData[b].attended - hostData[a].attended


  makeTable = () ->
    table = document.createElement('table')
    table.id = 'att-table'
    table.classList.add('table')
    table.classList.add('table-hover')

    thead = document.createElement('thead')
    theadRow = document.createElement('tr')
    nameTh = document.createElement('th')
    nameTh.innerText = 'Name'
    theadRow.appendChild(nameTh)
    ratioTh = document.createElement('th')
    ratioTh.innerText = 'Percent attendance (total attended)'
    theadRow.appendChild(ratioTh)
    thead.appendChild(theadRow)
    table.appendChild(thead)

    table.appendChild(makeTbody())
    table


  makeTbody = (page=1, perPage=5, hosts=orderedHosts) ->
    pagedHostNames = hosts.slice((page-1)*perPage, (page*perPage))
    tbody = document.createElement('tbody')
    tbody.id = 'att-tbody'

    for host in pagedHostNames
      tr = document.createElement('tr')
      name = document.createElement('td')
      name.innerText = host
      tr.appendChild(name)
      ratio = document.createElement('td')
      ratio.innerText = "#{Math.round(hostData[host]['attended']*100)}% (#{hostData[host]['listed']})"
      ratio.classList.add('text-right')
      tr.appendChild(ratio)
      tbody.appendChild(tr)

    tbody


  makePages = () ->
    paginationElt = document.getElementsByClassName('pagination')[0]
    numPages = Math.ceil(orderedHosts.length/5)
    for page in [0..numPages-1]
      pElt = document.createElement('li')
      pElt.classList.add('att-pg')
      pElt.setAttribute('data-page', page + 1)
      pElt.addEventListener 'click', (e) ->
        document.querySelectorAll('li.att-pg.active')[0].classList.remove('active')
        @classList.add('active')
        newBody = makeTbody @getAttribute('data-page')
        document.getElementById('att-tbody').remove()
        document.getElementById('att-table').appendChild(newBody)
      pAElt = document.createElement('a')
      pAElt.href = 'javascript:void(0)'
      pAElt.innerText = page + 1
      pElt.appendChild(pAElt)
      if page == 0
        pElt.classList.add 'active'
      paginationElt.appendChild(pElt)


  attendanceTable = document.getElementById('host-attendance')
  attendanceTable.getElementsByClassName('loading')[0].remove()
  attendanceTable.appendChild(makeTable())
  makePages()


showAttendanceNew = (data) =>
  ctx = document.getElementById('rawAttendance')

  showed_up = data.attendance_raw

  new Chart(ctx, {
    type: 'doughnut'
    data:
      datasets: [
        {
          data: Object.values(showed_up)
          backgroundColor: ['rgb(200, 200, 0)', 'rgb(200, 0, 200)', 'rgb(0, 200, 200)', 'rgb(200, 200, 200)']
        }
      ],
      labels: ['Girl No Shows', 'Lady Guests', 'Dude No Shows', 'Homies Who Came Through'],
  })


showPopulationChart = (data) =>
  ctx = document.getElementById("myChart")

  male_population = data.gender_population.male
  female_population = data.gender_population.female
  buckets = data.population

  max = Math.max.apply(Math, (b.population for b in buckets))

  chart = new Chart(ctx, {
    type: 'line'
    data: {
      labels: ((new Date(bucket.time)).toTimeString() for bucket in buckets)
      datasets: [
        {
          label: 'Total'
          data: (bucket.population for bucket in buckets)
          fill: false
          pointHitRadius: 15
          borderColor: 'rgb(75, 75, 75)'
          lineTension: 0.1
        },
        {
          label: 'Guys'
          data: (bucket.population for bucket in male_population)
          fill: true
          pointHitRadius: 15
          backgroundColor: 'rgba(91, 109, 227, 0.5)'
          borderColor: 'rgb(91, 109, 227)'
          lineTension: 0.1
        },
        {
          label: 'Girls'
          data: (bucket.population for bucket in female_population)
          fill: true
          pointHitRadius: 15
          backgroundColor: 'rgba(200, 91, 227, 0.5)'
          borderColor: 'rgb(200, 91, 227)'
          lineTension: 0.1
        },
      ]
    }
    options:
      scales:
        yAxes: [{
          ticks:
            max: Math.ceil(max * 1.2)
            beginAtZero: true
        }]
  })

$.get('report/data').done((res) ->
  showTotalAttendance res
  showHostGuestAttendance res
  showPopulationChart res
  showAttendanceNew res
)
