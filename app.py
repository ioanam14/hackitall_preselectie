import json

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


class Seat:
    def __init__(self, stations, seat_no):
        self.seat_no = seat_no
        self.no_stations = stations
        self.busy_stations = [False] * stations

    def verify_if_free(self, start, end):
        for i in range(start, end):
            if self.busy_stations[i]:
                return True
        return False

    def set_busy(self, start, end):
        for i in range(start, end):
            self.busy_stations[i] = True

    def __str__(self):
        return str(self.seat_no)


class Compartment:
    def __init__(self, no_seats, comp_no):
        self.comp_no = comp_no
        self.free_places = no_seats
        self.no_seats = no_seats
        self.seats = []
        for i in range(no_seats):
            self.seats.append(Seat(6, self.comp_no * 8 + i + 1))

    def verify_free_seats(self, no, start, end):
        no_seats_to_verify = no
        list = []
        for i in self.seats:
            busy = i.verify_if_free(start, end)
            if busy is False:
                list.append(i)
                no_seats_to_verify = no_seats_to_verify - 1
                if no_seats_to_verify == 0:
                    return list

        if no_seats_to_verify != 0:
            return []

    def get_all_free_seats(self, start, end):
        list = []
        for i in self.seats:
            if i.verify_if_free(start, end) is False:
                list.append(i.seat_no)
        return list

    def __str__(self):
        return str(self.comp_no + 1)

    def get_free_places_between_two_stations(self, start, end):
        no = 0
        for i in self.seats:
            busy = i.verify_if_free(start, end)
            if busy is False:
                no += 1
        return no


class Carriage:
    def __init__(self, no_compartments, carriage_no):
        self.carriage_no = carriage_no
        self.no_compartments = no_compartments
        self.compartments = []
        for i in range(no_compartments):
            self.compartments.append(Compartment(8, i))

    def __str__(self):
        return str(self.carriage_no)

    def get_free_seats_between_stations(self, start, end):
        free_seats = []
        for c in self.compartments:
            l = c.get_all_free_seats(start, end)
            free_seats = free_seats + l
        return free_seats


class Train:
    def __init__(self, no_carriages):
        self.no_carriages = no_carriages
        self.carriages = []
        for i in range(no_carriages):
            self.carriages.append(Carriage(10, i))


train = Train(5)
listTickets = [[[5], [2, 3], [4, 1], [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1, 1]],
               [[4], [2, 2], [3, 1], [2, 1, 1], [1, 1, 1, 1]], [[3], [2, 1], [1, 1, 1]], [[2], [1, 1]], [[1]]]


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/buy', methods=['POST'])
def split():
    try:
        data = json.loads(request.data)
    except Exception:
        return jsonify({'success': False})

    nr_tickets = int(data['numberOfPersons'])
    start = int(data['start'])
    end = int(data['end'])
    ok = True
    index = 5 - nr_tickets
    seatDict = []

    if nr_tickets < 1 or nr_tickets > 5:
        return jsonify({'success': False, 'message': 'The number of tickets must be between 1 and 5'})

    if start >= end:
        return jsonify({'success': False, 'message': 'Destination must be after the starting point'})

    for listPossibilities in listTickets[index]:
        ok = True
        for tickets in listPossibilities:
            best_carriage, best_compartment, sets_list = buy(tickets, start, end)
            if len(sets_list) > 0:
                seatDict.append({
                    'carriage': best_carriage,
                    'compartment': best_compartment,
                    'seats': sets_list
                })
            else:
                seatDict = []
                ok = False
                break
        if ok is True:
            break

    if len(seatDict) == 0:
        print("There are no more seats")
        return jsonify({'success': False, 'message': 'There are no more seats'})
    else:
        for value in seatDict:
            for key, val in value.items():
                if key == 'carriage' or key == 'compartment':
                    print(key, val)
                else:
                    for i in val:
                        print(i)
        print('\n')
        return jsonify({'success': True, 'data': seatDict})


def buy(nr_tickets, start, end):
    best_carriage = -1
    min_seats = 10
    best_compartment = -1
    seats_list = []
    for carriage in train.carriages:
        for compartment in carriage.compartments:
            free_places = compartment.get_free_places_between_two_stations(start, end)
            if free_places >= nr_tickets:
                list = compartment.verify_free_seats(nr_tickets, start, end)
                if len(list) > 0:
                    if min_seats > (8 - free_places) + nr_tickets:
                        min_seats = (8 - free_places) + nr_tickets
                        best_compartment = compartment
                        best_carriage = carriage.carriage_no
                        seats_list = list

    final_list = []
    if len(seats_list) > 0:
        for seat in seats_list:
            seat.set_busy(start, end)
            final_list.append(seat.seat_no)
        return best_carriage, best_compartment.comp_no + 1, final_list
    else:
        return -1, -1, []


@app.route('/get-free-seats', methods=['POST'])
def get_all_free_seats():
    try:
        data = json.loads(request.data)
    except Exception:
        return jsonify({'success': False})

    start = int(data['start'])
    end = int(data['end'])
    free_seats = []
    for carriage in train.carriages:
        l = carriage.get_free_seats_between_stations(start, end)
        dictVal = {
            'carriage': carriage.carriage_no,
            'seats': l
        }
        free_seats.append(dictVal)
    return free_seats


if __name__ == '__main__':
    app.run()
