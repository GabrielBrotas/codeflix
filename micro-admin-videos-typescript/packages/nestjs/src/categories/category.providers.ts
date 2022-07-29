/* eslint-disable @typescript-eslint/no-namespace */
import {
  CreateCategoryUseCase,
  UpdateCategoryUseCase,
  GetCategoryUseCase,
  ListCategoriesUseCase,
  DeleteCategoryUseCase,
} from '@gb/core/dist/application/use-cases';
import CategoryRepository from '@gb/core/dist/domain/category/repository/category.repository';
import { CategoryInMemoryRepository } from '@gb/core/dist/infra/category';

export namespace CATEGORY_PROVIDERS {
  export namespace REPOSITORIES {
    export const CATEGORY_IN_MEMORY_REPOSITORY = {
      provide: 'CategoryInMemoryRepository',
      useClass: CategoryInMemoryRepository,
    };
  }

  export namespace USE_CASES {
    export const CREATE_CATEGORY_USE_CASE = {
      provide: CreateCategoryUseCase.UseCase,
      useFactory: (categoryRepo: CategoryRepository.Repository) => {
        return new CreateCategoryUseCase.UseCase(categoryRepo);
      },
      inject: [REPOSITORIES.CATEGORY_IN_MEMORY_REPOSITORY.provide],
    };

    export const UPDATE_CATEGORY_USE_CASE = {
      provide: UpdateCategoryUseCase.UseCase,
      useFactory: (categoryRepo: CategoryRepository.Repository) => {
        return new UpdateCategoryUseCase.UseCase(categoryRepo);
      },
      inject: [REPOSITORIES.CATEGORY_IN_MEMORY_REPOSITORY.provide],
    };

    export const LIST_CATEGORIES_USE_CASE = {
      provide: ListCategoriesUseCase.UseCase,
      useFactory: (categoryRepo: CategoryRepository.Repository) => {
        return new ListCategoriesUseCase.UseCase(categoryRepo);
      },
      inject: [REPOSITORIES.CATEGORY_IN_MEMORY_REPOSITORY.provide],
    };

    export const GET_CATEGORY_USE_CASE = {
      provide: GetCategoryUseCase.UseCase,
      useFactory: (categoryRepo: CategoryRepository.Repository) => {
        return new GetCategoryUseCase.UseCase(categoryRepo);
      },
      inject: [REPOSITORIES.CATEGORY_IN_MEMORY_REPOSITORY.provide],
    };

    export const DELETE_CATEGORY_USE_CASE = {
      provide: DeleteCategoryUseCase.UseCase,
      useFactory: (categoryRepo: CategoryRepository.Repository) => {
        return new DeleteCategoryUseCase.UseCase(categoryRepo);
      },
      inject: [REPOSITORIES.CATEGORY_IN_MEMORY_REPOSITORY.provide],
    };
  }
}
