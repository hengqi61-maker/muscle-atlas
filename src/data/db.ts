import Dexie,{type EntityTable} from 'dexie';
import type {WorkoutSession,PlannedWorkout} from '../types/domain';
export const db=new Dexie('muscle-atlas') as Dexie & {sessions:EntityTable<WorkoutSession,'id'>;plans:EntityTable<PlannedWorkout,'id'>};
db.version(1).stores({sessions:'id,date',plans:'id,date,calendarEventId'});
export function completedCounts(sessions:WorkoutSession[]){return sessions.reduce((n,s)=>n+s.sets.filter(x=>x.exerciseId==='dumbbell-curl').length,0);}
