export type Staff = {
  id: number
  name: string
  age: number
  position: string
}

export type NewStaff = Omit<Staff, 'id'>

