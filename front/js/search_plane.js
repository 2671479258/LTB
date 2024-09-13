document.addEventListener('DOMContentLoaded', function() {
    const results = JSON.parse(localStorage.getItem('searchResults')) || [];
    const departureCity = localStorage.getItem('departureCity') || '';
    const destinationCity = localStorage.getItem('destinationCity') || '';
    const departureDate = localStorage.getItem('departureDate') || '';

    console.log('Initializing Vue instance');
    new Vue({
        el: '#app',
        data: {
            results: results,
            departureCity: departureCity,
            destinationCity: destinationCity,
            departureDate: departureDate
        },
        methods: {
            bookTicket(id) {
                console.log('bookTicket method called with id:', id);
                window.location.href = `flight_detail.html?id=${id}`;
            }
        },
        mounted() {
            console.log('Vue instance mounted');
        }
    });
});