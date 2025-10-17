# GitHub Copilot Instructions - Frontend (Angular/TypeScript)

## 🎨 Frontend Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── core/              # Core services (singleton)
│   │   │   ├── services/
│   │   │   │   ├── api.service.ts
│   │   │   │   └── notification.service.ts
│   │   │   └── interceptors/
│   │   │       └── http-error.interceptor.ts
│   │   ├── shared/            # Shared components
│   │   │   ├── components/
│   │   │   │   ├── card-preview/
│   │   │   │   ├── card-form/
│   │   │   │   ├── status-badge/
│   │   │   │   └── image-viewer/
│   │   │   └── models/
│   │   │       ├── card.model.ts
│   │   │       └── image.model.ts
│   │   ├── features/          # Feature modules
│   │   │   ├── upload/
│   │   │   │   ├── upload.component.ts
│   │   │   │   └── upload.service.ts
│   │   │   ├── cards/
│   │   │   │   ├── card-list/
│   │   │   │   ├── card-detail/
│   │   │   │   ├── card-edit/
│   │   │   │   └── cards.service.ts
│   │   │   └── validation/
│   │   │       └── validation.component.ts
│   │   ├── app.component.ts
│   │   └── app.routes.ts
│   ├── assets/
│   ├── environments/
│   │   ├── environment.ts
│   │   └── environment.prod.ts
│   └── styles.scss
├── angular.json
├── package.json
├── tsconfig.json
└── Dockerfile
```

---

## 📐 TypeScript Conventions

### Type Safety
Always use explicit types, avoid `any`:

```typescript
// ❌ Bad
function getCard(id: any): any {
  return this.http.get(`/api/cards/${id}`);
}

// ✅ Good
function getCard(id: number): Observable<Card> {
  return this.http.get<Card>(`${this.apiUrl}/cards/${id}`);
}
```

### Interfaces and Types
```typescript
export interface Card {
  id: number;
  nom: string;
  sous_titre?: string;
  encre?: 'Amber' | 'Amethyst' | 'Emerald' | 'Ruby' | 'Sapphire' | 'Steel';
  cout?: number;
  force?: number;
  volonte?: number;
  lore?: number;
  mots_cles: string[];
  texte?: string;
  rarete?: 'Common' | 'Uncommon' | 'Rare' | 'Super Rare' | 'Legendary' | 'Enchanted';
  status: CardStatus;
  created_at: string;
  updated_at: string;
}

export type CardStatus = 'non_traite' | 'en_cours' | 'attente_validation' | 'valide';

export interface CardListResponse {
  items: Card[];
  total: number;
  skip: number;
  limit: number;
}
```

---

## 🔧 Angular Patterns

### Service Pattern
```typescript
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@environments/environment';
import { Card, CardListResponse } from '@shared/models/card.model';

@Injectable({
  providedIn: 'root'
})
export class CardsService {
  private apiUrl = `${environment.apiUrl}/cards`;

  constructor(private http: HttpClient) {}

  getCards(skip: number = 0, limit: number = 100): Observable<CardListResponse> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    
    return this.http.get<CardListResponse>(this.apiUrl, { params });
  }

  getCard(id: number): Observable<Card> {
    return this.http.get<Card>(`${this.apiUrl}/${id}`);
  }

  updateCard(id: number, card: Partial<Card>): Observable<Card> {
    return this.http.put<Card>(`${this.apiUrl}/${id}`, card);
  }

  deleteCard(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
```

### Component Pattern
```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import { CardsService } from './cards.service';
import { Card } from '@shared/models/card.model';

@Component({
  selector: 'app-card-list',
  templateUrl: './card-list.component.html',
  styleUrls: ['./card-list.component.scss']
})
export class CardListComponent implements OnInit, OnDestroy {
  cards: Card[] = [];
  loading = false;
  error: string | null = null;
  
  private destroy$ = new Subject<void>();

  constructor(private cardsService: CardsService) {}

  ngOnInit(): void {
    this.loadCards();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadCards(): void {
    this.loading = true;
    this.error = null;

    this.cardsService
      .getCards()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          this.cards = response.items;
          this.loading = false;
        },
        error: (error) => {
          this.error = 'Failed to load cards';
          this.loading = false;
          console.error('Error loading cards:', error);
        }
      });
  }
}
```

---

## 🎯 Reactive Programming (RxJS)

### Common Operators
```typescript
import { map, filter, catchError, switchMap, debounceTime } from 'rxjs/operators';
import { of } from 'rxjs';

// Search with debounce
searchControl.valueChanges.pipe(
  debounceTime(300),
  filter(query => query.length > 2),
  switchMap(query => this.cardsService.search(query)),
  catchError(error => {
    console.error('Search failed:', error);
    return of([]);
  })
).subscribe(results => this.searchResults = results);
```

### Avoiding Memory Leaks
```typescript
// ✅ Good: Unsubscribe with takeUntil
this.cardsService.getCards()
  .pipe(takeUntil(this.destroy$))
  .subscribe(cards => this.cards = cards);

// ✅ Good: Async pipe (auto unsubscribe)
cards$ = this.cardsService.getCards();

// In template:
// <div *ngFor="let card of cards$ | async">
```

---

## 🎨 Naming Conventions

### Files and Folders
- Components: `card-list.component.ts` (kebab-case)
- Services: `cards.service.ts` (kebab-case)
- Models: `card.model.ts` (kebab-case)
- Folders: `card-list/` (kebab-case)

### Code
- Classes: `CardListComponent` (PascalCase)
- Interfaces: `Card`, `CardListResponse` (PascalCase)
- Variables/functions: `getCards`, `cardList` (camelCase)
- Constants: `API_URL`, `MAX_FILE_SIZE` (UPPER_SNAKE_CASE)

---

## 📝 Form Handling

### Reactive Forms
```typescript
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

export class CardFormComponent implements OnInit {
  cardForm: FormGroup;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.cardForm = this.fb.group({
      nom: ['', [Validators.required, Validators.maxLength(100)]],
      sous_titre: [''],
      encre: [''],
      cout: [null, [Validators.min(0), Validators.max(20)]],
      force: [null],
      volonte: [null],
      lore: [null],
      mots_cles: [[]],
      texte: [''],
      rarete: ['']
    });
  }

  onSubmit(): void {
    if (this.cardForm.valid) {
      const card = this.cardForm.value;
      this.cardsService.updateCard(this.cardId, card).subscribe({
        next: () => this.notificationService.success('Card updated'),
        error: (error) => this.notificationService.error('Update failed')
      });
    }
  }
}
```

---

## 🖼️ File Upload

### Upload Component
```typescript
@Component({
  selector: 'app-upload',
  template: `
    <div class="upload-zone" 
         (drop)="onDrop($event)" 
         (dragover)="onDragOver($event)"
         (dragleave)="onDragLeave($event)">
      <input type="file" 
             #fileInput 
             (change)="onFileSelected($event)" 
             accept="image/png,image/jpeg"
             hidden>
      <button (click)="fileInput.click()">Select Image</button>
    </div>
  `
})
export class UploadComponent {
  selectedFile: File | null = null;

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      this.uploadFile();
    }
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    if (event.dataTransfer?.files && event.dataTransfer.files.length > 0) {
      this.selectedFile = event.dataTransfer.files[0];
      this.uploadFile();
    }
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
  }

  uploadFile(): void {
    if (!this.selectedFile) return;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.uploadService.upload(formData).subscribe({
      next: (response) => console.log('Upload successful', response),
      error: (error) => console.error('Upload failed', error)
    });
  }
}
```

---

## 🎨 UI Framework

### Standalone Components (Angular 17+)
```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-status-badge',
  standalone: true,
  imports: [CommonModule],
  template: `
    <span [class]="'badge badge-' + status">
      {{ status | titlecase }}
    </span>
  `,
  styles: [`
    .badge {
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
    }
    .badge-valide { background: #10b981; color: white; }
    .badge-attente_validation { background: #f59e0b; color: white; }
    .badge-en_cours { background: #3b82f6; color: white; }
    .badge-non_traite { background: #6b7280; color: white; }
  `]
})
export class StatusBadgeComponent {
  @Input() status!: CardStatus;
}
```

---

## ⚠️ Error Handling

### HTTP Interceptor
```typescript
import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpErrorResponse } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { NotificationService } from '@core/services/notification.service';

@Injectable()
export class HttpErrorInterceptor implements HttpInterceptor {
  constructor(private notificationService: NotificationService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler) {
    return next.handle(req).pipe(
      catchError((error: HttpErrorResponse) => {
        let errorMessage = 'An error occurred';
        
        if (error.error instanceof ErrorEvent) {
          // Client-side error
          errorMessage = error.error.message;
        } else {
          // Server-side error
          errorMessage = error.error?.detail || error.message;
        }
        
        this.notificationService.error(errorMessage);
        return throwError(() => error);
      })
    );
  }
}
```

---

## 🧪 Testing

### Unit Tests
```typescript
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { CardsService } from './cards.service';

describe('CardsService', () => {
  let service: CardsService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [CardsService]
    });
    service = TestBed.inject(CardsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should fetch cards', () => {
    const mockCards = { items: [], total: 0, skip: 0, limit: 100 };

    service.getCards().subscribe(cards => {
      expect(cards).toEqual(mockCards);
    });

    const req = httpMock.expectOne(`${service['apiUrl']}`);
    expect(req.request.method).toBe('GET');
    req.flush(mockCards);
  });
});
```

---

## 🌍 Environment Configuration

```typescript
// environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};

// environment.prod.ts
export const environment = {
  production: true,
  apiUrl: '/api'  // Proxied through Nginx
};
```

---

## 🚀 Best Practices

### Performance
- Use `OnPush` change detection when possible
- Lazy load feature modules
- Use `trackBy` with `*ngFor`
- Unsubscribe from observables (use `takeUntil` or async pipe)

### Accessibility
- Use semantic HTML
- Add ARIA labels
- Ensure keyboard navigation

### Code Quality
- Keep components small and focused
- Extract reusable logic into services
- Use interfaces for type safety
- Write unit tests for critical functionality
